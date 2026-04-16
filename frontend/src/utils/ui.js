export const ui_toast = (message, type = 'info') => 
{
    const new_toast = document.createElement('onyks-toast');
    new_toast.textContent = message;
    new_toast.type = type;
    document.body.appendChild(new_toast);
};