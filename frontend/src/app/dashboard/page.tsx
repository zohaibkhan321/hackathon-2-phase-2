'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '../../components/TaskList';
import TaskForm from '../../components/TaskForm';
import { apiClient } from '../../lib/api';

const DashboardPage = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const data = await apiClient.getTasks();
      setTasks(data as any[]);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask) => {
    setTasks([newTask, ...tasks]);
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <div className="flex-1 min-w-0">
          <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
            My Tasks
          </h2>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TaskList
            tasks={tasks}
            onTaskUpdated={handleTaskUpdated}
            onTaskDeleted={handleTaskDeleted}
          />
        </div>
        <div>
          <TaskForm onTaskCreated={handleTaskCreated} />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;