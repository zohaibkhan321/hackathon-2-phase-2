import React, { useState } from 'react';
import { apiClient } from '@/lib/api';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onTaskUpdated, onTaskDeleted }) => {
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editText, setEditText] = useState('');

  const handleToggleComplete = async (task: Task) => {
    try {
      const updatedTask = (await apiClient.toggleTaskCompletion(task.id, !task.completed)) as Task;
      onTaskUpdated(updatedTask);
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await apiClient.deleteTask(taskId);
      onTaskDeleted(taskId);
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const startEditing = (task: Task) => {
    setEditingTaskId(task.id);
    setEditText(task.title);
  };

  const saveEdit = async (taskId: string) => {
    if (!editText.trim()) return;

    try {
      const updatedTask = (await apiClient.updateTask(taskId, { title: editText })) as Task;
      onTaskUpdated(updatedTask);
      setEditingTaskId(null);
      setEditText('');
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const cancelEdit = () => {
    setEditingTaskId(null);
    setEditText('');
  };

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-gray-200">
        {tasks.length === 0 ? (
          <li className="px-4 py-4 sm:px-6">
            <p className="text-gray-500">No tasks yet. Create your first task!</p>
          </li>
        ) : (
          tasks.map((task) => (
            <li key={task.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2">
                <div className="flex items-start md:items-center gap-2">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleComplete(task)}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mt-1 md:mt-0"
                  />
                  <div className="flex-1 min-w-0">
                    {editingTaskId === task.id ? (
                      <div className="flex flex-col sm:flex-row sm:items-center gap-2">
                        <input
                          type="text"
                          value={editText}
                          onChange={(e) => setEditText(e.target.value)}
                          className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-md p-1"
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') saveEdit(task.id);
                            if (e.key === 'Escape') cancelEdit();
                          }}
                        />
                        <div className="flex space-x-1">
                          <button
                            onClick={() => saveEdit(task.id)}
                            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                          >
                            Save
                          </button>
                          <button
                            onClick={cancelEdit}
                            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-gray-600 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div>
                        <p
                          className={`text-sm font-medium ${
                            task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                          }`}
                          onDoubleClick={() => startEditing(task)}
                        >
                          {task.title}
                        </p>
                        {task.description && (
                          <p className="text-sm text-gray-500 mt-1 truncate">{task.description}</p>
                        )}
                      </div>
                    )}
                    <div className="mt-1 text-xs text-gray-500 md:hidden">
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
                <div className="flex flex-shrink-0 space-x-2">
                  <button
                    onClick={() => startEditing(task)}
                    className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(task.id)}
                    className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Delete
                  </button>
                </div>
                <div className="hidden md:block text-xs text-gray-500">
                  Created: {new Date(task.created_at).toLocaleDateString()}
                </div>
              </div>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default TaskList;