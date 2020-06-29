# -*- coding: utf-8 -*-


"""Система анимации."""


class _Node(object):
    
    __slots__ = ("func", "curr_jobs", "next_jobs")
    
    def __init__(self, func):
        
        self.func = func
        self.curr_jobs = []
        self.next_jobs = []
    
    def __iter__(self):
        
        yield self.func
        yield self.curr_jobs


class Animachine(object):
    
    def __init__(self):
        
        self.st = None
        self.groups = {}
        self.jobs_count = 0
    
    def register(self, group, func):
        
        self.groups[group] = _Node(func)
    
    def remove(self, group):
        
        if group in self.groups:
            self.jobs_count -= len(self.groups[group].curr_jobs)
            del self.groups[group]
    
    def is_over(self, group):
        
        return not bool(self.groups[group].curr_jobs)
    
    def plan_job(self, group, args):
        
        self.groups[group].curr_jobs.append(args)
        self.jobs_count += 1
    
    def animate(self, st):
        
        if self.jobs_count == 0:
            return False
        
        if self.st is None:
            self.st = st
            return True
        
        dt = st - self.st
        
        for group in self.groups:
            node = self.groups[group]
            func, jobs = node
            while jobs:
                args = jobs.pop()
                self.jobs_count -= 1
                next_args = func(dt, *args)
                if next_args is not None:
                    node.next_jobs.append(next_args)
            node.curr_jobs, node.next_jobs = \
                node.next_jobs, node.curr_jobs
            self.jobs_count += len(node.curr_jobs)
        
        self.st = None if self.jobs_count == 0 else st
        
        return True
