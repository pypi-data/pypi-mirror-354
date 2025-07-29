#!/usr/bin/python3

# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import multiprocessing
import time
import queue
import socket
import uuid
import json

from . import data_sender_thread
from . import udp_initial_string_sender_thread
from . import data_receiver_thread
from . import control_receiver_thread
from . import util
from . import const
from . import output
from . import graph
from . import tcp_helper

from .tcp_control_connection_class import TcpControlConnectionClass


def client_mainline(args):
    client_start_time = time.time()

    if args.verbosity:
        print("args: {}".format(args), flush=True)

    server_ip = args.client
    server_port = args.port
    server_addr = (server_ip, server_port)

    # create control connection

    if args.verbosity:
        print("creating control connection to server at {}".format(server_addr), flush=True)

    control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_sock.connect(server_addr)

    control_conn = TcpControlConnectionClass(control_sock)
    control_conn.set_args(args)

    client_control_addr = control_sock.getsockname()

    if args.verbosity:
        print("created control connection, client {}, server {}".format(
              client_control_addr, server_addr), flush=True)

    # generate a random UUID (36 character string)
    run_id = str(uuid.uuid4())
    control_initial_string = "control " + run_id

    if args.verbosity:
        print("sending control initial string: {}".format(control_initial_string), flush=True)

    control_conn.send_string(control_initial_string)

    if args.verbosity:
        print("sent control initial string", flush=True)

    if args.verbosity:
        print("sending args to server: {}".format(vars(args)), flush=True)

    args_json = json.dumps(vars(args))
    control_conn.send_string(args_json)

    if args.verbosity:
        print("sent args to server", flush=True)

    # create data connection

    if args.verbosity:
        print("creating data connection to server at {}".format(server_addr), flush=True)

    data_initial_string = "data " + run_id

    if args.udp:
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data_sock.settimeout(const.SOCKET_TIMEOUT_SEC)
        client_data_addr = data_sock.getsockname()
        if args.verbosity:
            print("created udp data connection, client {}, no server addr".format(client_data_addr), flush=True)

        if args.verbosity:
            print("sending data initial string (async udp): {}".format(data_initial_string), flush=True)
        # start and keep sending the data connection initial string asynchronously
        shared_initial_string_done = multiprocessing.Value('i', 0)
        data_udp_ping_sender_process = multiprocessing.Process(
            name = "datainitialsender",
            target = udp_initial_string_sender_thread.run,
            args = (args, data_sock, server_addr, data_initial_string, shared_initial_string_done),
            daemon = True)
        data_udp_ping_sender_process.start()

    else:
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_helper.set_congestion_control(data_sock)
        data_sock.connect(server_addr)
        data_sock.settimeout(const.SOCKET_TIMEOUT_SEC)
        client_data_addr = data_sock.getsockname()
        if args.verbosity:
            print("created tcp data connection, client {}, server {}".format(
                client_data_addr, server_addr), flush=True)

        if args.verbosity:
            print("sending data initial string (tcp): {}".format(data_initial_string), flush=True)
        tcp_helper.send_string(args, data_sock, data_initial_string)
        if args.verbosity:
            print("sent data initial string (tcp)", flush=True)

    if args.verbosity:
        print("waiting for connection setup complete message from server", flush=True)
    # wait for connection setup complete message
    len_of_setup_complete_message = len(const.SETUP_COMPLETE_MSG)
    payload_bytes = tcp_helper.recv_exact_num_bytes(control_sock, len_of_setup_complete_message)
    payload_str = payload_bytes.decode()
    if payload_str != const.SETUP_COMPLETE_MSG:
        raise Exception("ERROR: client_mainline: setup complete message was not received")

    if args.udp:
        shared_initial_string_done.value = 1

    if args.verbosity:
        print("connection setup complete message received from server", flush=True)

    shared_run_mode = multiprocessing.Value('i', const.RUN_MODE_CALIBRATING)
    shared_udp_sending_rate_pps = multiprocessing.Value('d', const.UDP_DEFAULT_INITIAL_RATE)
    control_receiver_results_queue = multiprocessing.Queue()

    if not args.reverse:
        # up direction

        control_receiver_process = multiprocessing.Process(
            name = "controlreceiver",
            target = control_receiver_thread.run_recv_term_queue,
            args = (args, control_conn, control_receiver_results_queue, shared_run_mode, shared_udp_sending_rate_pps),
            daemon = True)

        control_receiver_process.start()

        data_sender_process = multiprocessing.Process(
            name = "datasender",
            target = data_sender_thread.run,
            args = (args, data_sock, server_addr, shared_run_mode, shared_udp_sending_rate_pps),
            daemon = True)

        # test starts here
        data_sender_process.start()

        thread_list = []
        thread_list.append(control_receiver_process)
        thread_list.append(data_sender_process)

    if args.reverse:
        # down direction

        data_receiver_process = multiprocessing.Process(
            name = "datareceiver",
            target = data_receiver_thread.run,
            args = (args, control_conn, data_sock, server_addr),
            daemon = True)

        data_receiver_process.start()

        control_receiver_process = multiprocessing.Process(
            name = "controlreceiver",
            target = control_receiver_thread.run_recv_queue,
            args = (args, control_conn, control_receiver_results_queue),
            daemon = True)

        control_receiver_process.start()

        # test starts here

        if args.verbosity:
            print("sending start message to server", flush=True)

        control_conn.send_string(const.START_MSG)

        if args.verbosity:
            print("sent start message to server", flush=True)

        thread_list = []
        thread_list.append(data_receiver_process)
        thread_list.append(control_receiver_process)

    if args.verbosity:
        print("test running, {} {}, control conn addr {}, data conn addr {}, server addr {}, elapsed startup time {} seconds".format(
              "udp" if args.udp else "tcp",
              "down" if args.reverse else "up",
              client_control_addr,
              client_data_addr,
              server_addr,
              (time.time() - client_start_time)),
              flush=True)

    # output loop

    output.init(args)

    while True:
        try:
            s1 = control_receiver_results_queue.get_nowait()
        except queue.Empty:
            s1 = None

        if s1:
            output.print_output(s1)
            continue

        if util.threads_are_running(thread_list):
            # nothing in queues, but test is still running
            time.sleep(0.01)
            continue
        else:
            break

    if args.verbosity:
        print("test finished, generating output", flush=True)

    output.term()

    util.done_with_socket(data_sock)
    util.done_with_socket(control_sock)

    graphdatafilename = output.get_graph_data_file_name()
    rawdatafilename = output.get_raw_data_file_name()

    if args.graph and not args.quiet:
        graph.create_graph(args, graphdatafilename)
        print("created graph: {}".format(graphdatafilename + ".png"), flush=True)

    if args.keep and not args.quiet:
        print("keeping graph data file: {}".format(graphdatafilename), flush=True)
        print("keeping raw data file: {}".format(rawdatafilename), flush=True)
    else:
        output.delete_data_files()

    if args.verbosity:
        print("test complete, exiting")
