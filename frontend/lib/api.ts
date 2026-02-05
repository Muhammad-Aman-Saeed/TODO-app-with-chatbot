// Centralized API client with JWT handling
import { Task, User } from '@/types';

class ApiClient {
  private baseUrl: string;

  constructor() {
    // Ensure the base URL ends with '/api' if it's the root URL
    const envBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    if (envBaseUrl) {
      // If the environment variable is set, use it as is
      this.baseUrl = envBaseUrl;
    } else {
      // Default to the expected backend URL
      this.baseUrl = 'http://localhost:8000/api';
    }
  }

  // Helper to get JWT token
  private getJwtToken(): string | null {
    // Implementation to retrieve JWT from storage or session
    if (typeof window !== 'undefined') {
      // Client-side: get from localStorage or session
      const token = localStorage.getItem('jwt_token');
      return token;
    }
    // Server-side: would need to implement differently
    return null;
  }

  // Generic request method that adds JWT header
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getJwtToken();

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        // If the error is 401, it means the token might be invalid or expired
        if (response.status === 401) {
          // Clear the invalid token from storage
          if (typeof window !== 'undefined') {
            localStorage.removeItem('jwt_token');
          }

          // Throw a specific error for 401
          throw new Error(`API request failed: ${response.status} - Unauthorized. Please log in again.`);
        }

        // For other errors, throw a generic error with status
        const errorText = await response.text(); // Get the error response text
        throw new Error(`API request failed: ${response.status} - ${errorText || response.statusText}`);
      }

      return response.json();
    } catch (error) {
      // Handle network errors (like "Failed to fetch")
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend server is running.');
      }
      throw error; // Re-throw other errors
    }
  }

  // Specific API methods
  async getTasks(): Promise<Task[]> {
    return this.request('/tasks/');
  }

  async createTask(taskData: Omit<Task, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<Task> {
    return this.request('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: number, taskData: Partial<Task>): Promise<Task> {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: number): Promise<void> {
    const token = this.getJwtToken();

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };

    try {
      const response = await fetch(`${this.baseUrl}/tasks/${id}`, {
        method: 'DELETE',
        headers,
      });

      if (!response.ok) {
        // If the error is 401, it means the token might be invalid or expired
        if (response.status === 401) {
          // Clear the invalid token from storage
          if (typeof window !== 'undefined') {
            localStorage.removeItem('jwt_token');
          }

          // Throw a specific error for 401
          throw new Error(`API request failed: ${response.status} - Unauthorized. Please log in again.`);
        }

        // For other errors, throw a generic error with status
        const errorText = await response.text(); // Get the error response text
        throw new Error(`API request failed: ${response.status} - ${errorText || response.statusText}`);
      }

      // For DELETE requests, we don't need to parse JSON if the response is 204 No Content
      if (response.status === 204) {
        return; // Simply return for 204 No Content
      }

      // If there's content to parse, parse it
      return response.json();
    } catch (error) {
      // Handle network errors (like "Failed to fetch")
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend server is running.');
      }
      throw error; // Re-throw other errors
    }
  }

  async toggleComplete(id: number, completed: boolean): Promise<Task> {
    return this.request(`/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }

  async chat(message: string, conversationId: number | null): Promise<ChatResponse> {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });
  }

  async getConversationHistory(conversationId: number): Promise<any[]> {
    return this.request(`/conversations/${conversationId}/messages`);
  }

}

// Define the response type for chat
export type ChatResponse = {
  action: 'add' | 'delete' | 'update' | 'complete' | 'list' | 'none';
  task: {
    id: string;
    title: string;
    description: string;
    completed: boolean;
  } | null;
  message: string;
  conversation_id: number;
};

// Export a convenience function for chat
export const chatAPI = async (message: string, conversationId: number | null = null) => {
  return apiClient.chat(message, conversationId);
};

export const apiClient = new ApiClient();