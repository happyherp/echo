function echoApp() {
    return {
        comments: [],
        loading: false,
        message: '',
        messageType: 'success',
        newComment: {
            email: '',
            content: ''
        },
        replyForm: {
            show: false,
            parentId: null,
            email: '',
            content: ''
        },

        async init() {
            await this.loadComments();
            // Auto-refresh comments every 10 seconds
            setInterval(() => this.loadComments(), 10000);
        },

        async loadComments() {
            try {
                const response = await fetch('/api/comments');
                if (response.ok) {
                    this.comments = await response.json();
                }
            } catch (error) {
                console.error('Failed to load comments:', error);
            }
        },

        async submitComment() {
            if (!this.newComment.email || !this.newComment.content) return;

            this.loading = true;
            try {
                const response = await fetch('/api/comments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.newComment)
                });

                if (response.ok) {
                    this.showMessage('Comment posted! Carlos will respond shortly.', 'success');
                    this.newComment = { email: '', content: '' };
                    await this.loadComments();
                } else {
                    const error = await response.json();
                    this.showMessage(error.detail || 'Failed to post comment', 'error');
                }
            } catch (error) {
                this.showMessage('Network error. Please try again.', 'error');
            } finally {
                this.loading = false;
            }
        },

        async submitReply() {
            if (!this.replyForm.email || !this.replyForm.content) return;

            this.loading = true;
            try {
                const response = await fetch('/api/comments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: this.replyForm.email,
                        content: this.replyForm.content,
                        parent_id: this.replyForm.parentId
                    })
                });

                if (response.ok) {
                    this.showMessage('Reply posted!', 'success');
                    this.closeReplyForm();
                    await this.loadComments();
                } else {
                    const error = await response.json();
                    this.showMessage(error.detail || 'Failed to post reply', 'error');
                }
            } catch (error) {
                this.showMessage('Network error. Please try again.', 'error');
            } finally {
                this.loading = false;
            }
        },

        showReplyForm(parentId) {
            this.replyForm = {
                show: true,
                parentId: parentId,
                email: '',
                content: ''
            };
        },

        closeReplyForm() {
            this.replyForm.show = false;
        },

        showMessage(text, type = 'success') {
            this.message = text;
            this.messageType = type;
            setTimeout(() => {
                this.message = '';
            }, 5000);
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString();
        },

        renderComment(comment, depth) {
            const maxDepth = 5;
            const isAI = comment.is_ai;
            const isFlagged = comment.is_flagged;
            
            let commentClass = 'comment';
            if (isAI) commentClass += ' ai';
            if (isFlagged) commentClass += ' flagged';

            let authorName = isAI ? '🤖 Carlos (AI)' : comment.email;
            let authorClass = isAI ? 'comment-author ai' : 'comment-author';

            let html = `
                <div class="${commentClass}">
                    <div class="comment-header">
                        <span class="${authorClass}">${authorName}</span>
                        <span class="comment-date">${this.formatDate(comment.created_at)}</span>
                    </div>
                    <div class="comment-content">${this.escapeHtml(comment.content)}</div>
            `;

            // Add reply button if not too deep and not AI comment
            if (depth < maxDepth && !isAI) {
                html += `
                    <div class="comment-actions">
                        <button class="btn-reply" onclick="window.echoAppInstance.showReplyForm(${comment.id})">
                            Reply
                        </button>
                    </div>
                `;
            }

            // Add children if they exist
            if (comment.children && comment.children.length > 0) {
                html += '<div class="comment-children">';
                comment.children.forEach(child => {
                    html += this.renderComment(child, depth + 1);
                });
                html += '</div>';
            }

            html += '</div>';
            return html;
        },

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    };
}

// Make the app instance globally available for button clicks
document.addEventListener('alpine:init', () => {
    window.echoAppInstance = null;
});

document.addEventListener('DOMContentLoaded', () => {
    // Store reference to the app instance
    const appElement = document.getElementById('app');
    if (appElement && appElement._x_dataStack) {
        window.echoAppInstance = appElement._x_dataStack[0];
    }
});