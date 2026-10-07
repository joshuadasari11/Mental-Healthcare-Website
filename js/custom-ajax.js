$(document).ready(function() {
  // Add Toast Container to body dynamically
  if ($('#toastContainer').length === 0) {
    $('body').append('<div class="toast-container" id="toastContainer" style="position: fixed; top: 20px; right: 20px; z-index: 9999;"></div>');
  }

  // Inject Toast CSS
  $('<style>')
    .prop('type', 'text/css')
    .html(`
      .custom-toast {
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border-left: 4px solid #00bbf0;
        color: #ffffff;
        min-width: 280px;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        padding: 15px 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: slideIn 0.3s ease forwards;
        font-family: sans-serif;
      }
      .custom-toast.error { border-left-color: #ff3366; }
      .custom-toast.success { border-left-color: #00ffcc; }
      @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
      @keyframes fadeOut { to { transform: translateY(-20px); opacity: 0; } }
    `)
    .appendTo('head');

  function showToast(message, type = 'info') {
    const container = $('#toastContainer');
    const toast = $('<div class="custom-toast ' + type + '"></div>');
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-triangle';

    toast.html(`
      <div>
        <i class="fa ${icon}" aria-hidden="true" style="margin-right: 10px;"></i>
        <span>${escapeHTML(message)}</span>
      </div>
      <i class="fa fa-times" aria-hidden="true" style="cursor: pointer; margin-left: 15px;" onclick="this.parentElement.remove()"></i>
    `);
    
    container.append(toast);
    
    setTimeout(() => {
      toast.css('animation', 'fadeOut 0.5s ease forwards');
      setTimeout(() => { toast.remove(); }, 500);
    }, 4000);
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, tag => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[tag] || tag));
  }

  // Handle Contact Form Submission
  $('#contactForm').on('submit', async function(e) {
    e.preventDefault();
    const submitBtn = $(this).find('input[type="submit"]');
    const originalText = submitBtn.val();
    
    submitBtn.prop('disabled', true).val('Sending...');

    const formData = {
      name: $(this).find('[name="name"]').val(),
      email: $(this).find('[name="email"]').val(),
      mobile_number: $(this).find('[name="mobile_number"]').val(),
      address: $(this).find('[name="address"]').val(),
      message: $(this).find('[name="message"]').val() || ''
    };

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const result = await response.json();
      
      if (response.ok && result.success) {
        showToast(result.message, 'success');
        $('#contactForm')[0].reset();
      } else {
        showToast(result.message || 'Error sending message', 'error');
      }
    } catch (err) {
      showToast('Network error, please try again.', 'error');
    } finally {
      submitBtn.prop('disabled', false).val(originalText);
    }
  });

  // Handle Subscribe Form Submission
  $('.subscribe-form').on('submit', async function(e) {
    e.preventDefault();
    const form = $(this);
    const input = form.find('input[type="email"]');
    const email = input.val();
    const submitBtn = form.find('button[type="submit"]');
    const originalText = submitBtn.text();

    if (!email) return;

    submitBtn.prop('disabled', true).text('...');

    try {
      const response = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      const result = await response.json();

      if (response.ok && result.success) {
        showToast(result.message, 'success');
        form[0].reset();
      } else {
        showToast(result.message || 'Error subscribing', 'error');
      }
    } catch (err) {
      showToast('Network error.', 'error');
    } finally {
      submitBtn.prop('disabled', false).text(originalText);
    }
  });
});
