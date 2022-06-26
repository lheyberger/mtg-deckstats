#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool as Pool


__all__ = []


logger = logging.getLogger(f'mtg_deckstats.{__name__}')


def run_graph(functions: dict, dependencies: dict) -> dict:

    def execute_task(key, deps):
        func = functions[key]
        args = [results[d] for d in deps if d in results]
        logger.debug('%sStarting task %s', " "*4, key)

        task_start = time.time()
        result = func(*args)
        duration = round(time.time() - task_start, 2)

        logger.debug('%sFinished task %s (duration %fs)', " "*4, key, duration)
        return key, result

    results = {}

    logger.debug('Starting report')
    report_start = time.time()

    while True:
        backlog = []

        # Select next batch of tasks
        for key, deps in dependencies.items():
            if key in results:
                continue
            if not deps or set(deps).issubset(results.keys()):
                backlog.append((key, deps))

        # Backlog is empty we have finished
        if not backlog:
            break

        # Backlog is not empty, let's run it
        logger.debug('%sStarting batch', " "*2)
        batch_start = time.time()
        nb_tasks = min(cpu_count() - 1, len(backlog))
        if nb_tasks > 1:
            # Investigate ProcessPoolExecutor and ThreadPoolExecutor
            with Pool(nb_tasks) as pool:
                backlog_results = pool.starmap(execute_task, backlog)
                for key, result in backlog_results:
                    results[key] = result
        else:
            for key, deps in backlog:
                key, result = execute_task(key, deps)
                results[key] = result

        batch_duration = round(time.time() - batch_start, 2)
        logger.debug('%sFinished batch (duration %fs)', " "*2, batch_duration)

    report_duration = round(time.time() - report_start, 2)
    logger.debug('Finished report (duration %fs)', report_duration)

    return results
