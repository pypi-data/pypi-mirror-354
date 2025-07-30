/**
 * Auto-completion and Checkpoint Management
 * ========================================
 * 
 * JavaScript untuk mengelola auto-completion dan checkpoint di Web UI
 */

class AutoCompletionManager {
    constructor() {
        this.isEnabled = false;
        this.config = {};
        this.history = [];
        this.checkpoints = [];
        this.refreshInterval = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadStatus();
        this.startAutoRefresh();
    }
    
    setupEventListeners() {
        // Auto-completion controls
        document.getElementById('enable-auto-completion')?.addEventListener('click', () => this.enableAutoCompletion());
        document.getElementById('disable-auto-completion')?.addEventListener('click', () => this.disableAutoCompletion());
        document.getElementById('reset-session')?.addEventListener('click', () => this.resetSession());
        document.getElementById('save-config')?.addEventListener('click', () => this.saveConfig());
        
        // Test controls
        document.getElementById('test-trigger')?.addEventListener('click', () => this.testTrigger());
        document.getElementById('clear-test')?.addEventListener('click', () => this.clearTest());
        
        // History controls
        document.getElementById('refresh-history')?.addEventListener('click', () => this.refreshHistory());
        document.getElementById('clear-history')?.addEventListener('click', () => this.clearHistory());
        
        // Checkpoint controls
        document.getElementById('create-checkpoint')?.addEventListener('click', () => this.createCheckpoint());
        document.getElementById('refresh-checkpoints')?.addEventListener('click', () => this.refreshCheckpoints());
        document.getElementById('enable-auto-checkpoint')?.addEventListener('change', (e) => this.toggleAutoCheckpoint(e.target.checked));
    }
    
    async enableAutoCompletion() {
        try {
            const response = await fetch('/api/auto-completion/enable', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Auto-completion enabled', 'success');
                this.loadStatus();
            } else {
                this.showMessage('Failed to enable auto-completion', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async disableAutoCompletion() {
        try {
            const response = await fetch('/api/auto-completion/disable', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Auto-completion disabled', 'success');
                this.loadStatus();
            } else {
                this.showMessage('Failed to disable auto-completion', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async resetSession() {
        try {
            const response = await fetch('/api/auto-completion/reset-session', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Session reset', 'success');
                this.loadStatus();
            } else {
                this.showMessage('Failed to reset session', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async saveConfig() {
        try {
            const config = {
                auto_trigger_delay: parseFloat(document.getElementById('auto-trigger-delay')?.value || 2),
                max_triggers_per_session: parseInt(document.getElementById('max-triggers-session')?.value || 5),
                cooldown_period: parseFloat(document.getElementById('cooldown-period')?.value || 30),
                require_confirmation: document.getElementById('require-confirmation')?.checked || false
            };
            
            const response = await fetch('/api/auto-completion/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Configuration saved', 'success');
                this.config = result.data;
            } else {
                this.showMessage('Failed to save configuration', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async testTrigger() {
        try {
            const text = document.getElementById('test-text')?.value;
            if (!text) {
                this.showMessage('Please enter text to test', 'warning');
                return;
            }
            
            const response = await fetch('/api/auto-completion/test-trigger', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            
            const result = await response.json();
            
            if (result.success) {
                document.getElementById('test-result').textContent = JSON.stringify(result.data, null, 2);
            } else {
                this.showMessage('Failed to test trigger', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    clearTest() {
        document.getElementById('test-text').value = '';
        document.getElementById('test-result').textContent = '';
    }
    
    async loadStatus() {
        try {
            const response = await fetch('/api/auto-completion/status');
            const result = await response.json();
            
            if (result.success) {
                this.updateStatusDisplay(result.data);
            }
        } catch (error) {
            console.error('Error loading status:', error);
        }
    }
    
    updateStatusDisplay(data) {
        const autoCompletion = data.auto_completion;
        const checkpoint = data.checkpoint;
        
        // Update status text
        const statusElement = document.getElementById('auto-completion-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="status-section">
                    <h4>Auto-completion Status</h4>
                    <p>Enabled: ${autoCompletion.enabled ? 'Yes' : 'No'}</p>
                    <p>Session Triggers: ${autoCompletion.session_trigger_count}</p>
                    <p>Total History: ${autoCompletion.total_trigger_history}</p>
                    <p>Last Trigger: ${autoCompletion.last_trigger_time > 0 ? new Date(autoCompletion.last_trigger_time * 1000).toLocaleString() : 'Never'}</p>
                </div>
                <div class="status-section">
                    <h4>Checkpoint Status</h4>
                    <p>Auto Enabled: ${checkpoint.auto_checkpoint_enabled ? 'Yes' : 'No'}</p>
                    <p>Auto Interval: ${checkpoint.auto_checkpoint_interval}s</p>
                    <p>Total Checkpoints: ${checkpoint.total_checkpoints}</p>
                </div>
            `;
        }
        
        // Update config inputs
        if (autoCompletion.config) {
            document.getElementById('auto-trigger-delay').value = autoCompletion.config.auto_trigger_delay;
            document.getElementById('max-triggers-session').value = autoCompletion.config.max_triggers_per_session;
            document.getElementById('cooldown-period').value = autoCompletion.config.cooldown_period;
            document.getElementById('require-confirmation').checked = autoCompletion.config.require_confirmation;
        }
        
        // Update checkpoint settings
        document.getElementById('enable-auto-checkpoint').checked = checkpoint.auto_checkpoint_enabled;
        document.getElementById('auto-checkpoint-interval').value = checkpoint.auto_checkpoint_interval;
        
        this.isEnabled = autoCompletion.enabled;
        this.config = autoCompletion.config;
    }
    
    async refreshHistory() {
        try {
            const response = await fetch('/api/auto-completion/history?limit=50');
            const result = await response.json();
            
            if (result.success) {
                this.displayHistory(result.data.history);
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    displayHistory(history) {
        const tbody = document.querySelector('#history-table tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        history.forEach(record => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${record.timestamp_str}</td>
                <td>${record.triggers.join(', ')}</td>
                <td title="${record.text}">${record.text.substring(0, 50)}${record.text.length > 50 ? '...' : ''}</td>
                <td>${JSON.stringify(record.context).substring(0, 30)}...</td>
            `;
        });
    }
    
    async clearHistory() {
        if (!confirm('Are you sure you want to clear trigger history?')) return;
        
        try {
            const response = await fetch('/api/auto-completion/history', { method: 'DELETE' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('History cleared', 'success');
                this.refreshHistory();
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async createCheckpoint() {
        try {
            const name = document.getElementById('checkpoint-name')?.value || '';
            const description = document.getElementById('checkpoint-description')?.value || '';
            
            const response = await fetch('/api/auto-completion/checkpoint/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name,
                    description,
                    project_directory: '.',
                    tags: ['manual', 'web']
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showMessage(`Checkpoint created: ${result.data.checkpoint_info.name}`, 'success');
                document.getElementById('checkpoint-name').value = '';
                document.getElementById('checkpoint-description').value = '';
                this.refreshCheckpoints();
            } else {
                this.showMessage('Failed to create checkpoint', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async refreshCheckpoints() {
        try {
            const response = await fetch('/api/auto-completion/checkpoint/list?limit=20');
            const result = await response.json();
            
            if (result.success) {
                this.displayCheckpoints(result.data.checkpoints);
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    displayCheckpoints(checkpoints) {
        const tbody = document.querySelector('#checkpoint-table tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        checkpoints.forEach(checkpoint => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${checkpoint.name}</td>
                <td>${checkpoint.type}</td>
                <td>${checkpoint.created_at_str}</td>
                <td>${checkpoint.file_count}</td>
                <td>
                    <button onclick="autoCompletionManager.restoreCheckpoint('${checkpoint.id}')" class="btn btn-sm btn-primary">Restore</button>
                    <button onclick="autoCompletionManager.deleteCheckpoint('${checkpoint.id}')" class="btn btn-sm btn-danger">Delete</button>
                </td>
                <td title="${checkpoint.id}">${checkpoint.id.substring(0, 8)}...</td>
            `;
        });
    }
    
    async restoreCheckpoint(checkpointId) {
        if (!confirm('Are you sure you want to restore this checkpoint?')) return;
        
        try {
            const response = await fetch(`/api/auto-completion/checkpoint/${checkpointId}/restore`, { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Checkpoint restored successfully', 'success');
            } else {
                this.showMessage('Failed to restore checkpoint', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async deleteCheckpoint(checkpointId) {
        if (!confirm('Are you sure you want to delete this checkpoint?')) return;
        
        try {
            const response = await fetch(`/api/auto-completion/checkpoint/${checkpointId}`, { method: 'DELETE' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage('Checkpoint deleted', 'success');
                this.refreshCheckpoints();
            } else {
                this.showMessage('Failed to delete checkpoint', 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async toggleAutoCheckpoint(enabled) {
        try {
            const endpoint = enabled ? '/api/auto-completion/checkpoint/auto/enable' : '/api/auto-completion/checkpoint/auto/disable';
            const response = await fetch(endpoint, { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage(`Auto checkpoint ${enabled ? 'enabled' : 'disabled'}`, 'success');
                
                // If enabling, also set interval
                if (enabled) {
                    const interval = parseInt(document.getElementById('auto-checkpoint-interval')?.value || 300);
                    await this.setAutoCheckpointInterval(interval);
                }
            } else {
                this.showMessage(`Failed to ${enabled ? 'enable' : 'disable'} auto checkpoint`, 'error');
            }
        } catch (error) {
            this.showMessage(`Error: ${error.message}`, 'error');
        }
    }
    
    async setAutoCheckpointInterval(interval) {
        try {
            const response = await fetch(`/api/auto-completion/checkpoint/auto/interval?interval=${interval}`, { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.showMessage(`Auto checkpoint interval set to ${interval} seconds`, 'success');
            }
        } catch (error) {
            console.error('Error setting auto checkpoint interval:', error);
        }
    }
    
    startAutoRefresh() {
        // Refresh status every 10 seconds
        this.refreshInterval = setInterval(() => {
            this.loadStatus();
        }, 10000);
    }
    
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
    
    showMessage(message, type = 'info') {
        // Create or update message element
        let messageElement = document.getElementById('auto-completion-message');
        if (!messageElement) {
            messageElement = document.createElement('div');
            messageElement.id = 'auto-completion-message';
            messageElement.className = 'alert';
            document.querySelector('.auto-completion-container')?.prepend(messageElement);
        }
        
        messageElement.className = `alert alert-${type}`;
        messageElement.textContent = message;
        messageElement.style.display = 'block';
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 5000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.autoCompletionManager = new AutoCompletionManager();
});
