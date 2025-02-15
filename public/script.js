document.addEventListener('DOMContentLoaded', () => {
  loadLinks();

  // Form submission handler
  const linkForm = document.getElementById('linkForm');
  linkForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const linkName = document.getElementById('linkName').value;
    const linkUrl = document.getElementById('linkUrl').value;

    await saveLink(linkName, linkUrl);
    loadLinks();
  });
});

// Save link to the backend
async function saveLink(linkName, linkUrl) {
  try {
    const response = await fetch('http://localhost:3000/saveLink', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ linkName, linkUrl }),
    });

    const data = await response.json();
    if (data.success) {
      alert('Link saved!');
    } else {
      alert('Failed to save the link');
    }
  } catch (error) {
    console.error('Error saving link:', error);
  }
}

// Load all links
async function loadLinks() {
  try {
    const response = await fetch('http://localhost:3000/links');
    const data = await response.json();

    const embeddedContent = document.getElementById('embeddedContent');
    embeddedContent.innerHTML = '';

    if (data.success && data.data.length > 0) {
      data.data.forEach(link => {
        embeddedContent.innerHTML += `
          <div class="post">
            <a href="${link.url}" target="_blank"><h2>${link.name}</h2></a>
            <button class="btn btn-danger" onclick="removeLink('${link._id}')">Remove</button>
          </div>
        `;
      });
    } else {
      embeddedContent.innerHTML = 'No links available.';
    }
  } catch (error) {
    console.error('Error loading links:', error);
  }
}

// Remove a link
async function removeLink(id) {
  try {
    const response = await fetch('http://localhost:3000/removeLink', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id }),
    });

    const data = await response.json();
    if (data.success) {
      alert('Link removed!');
      loadLinks();
    } else {
      alert('Failed to remove the link');
    }
  } catch (error) {
    console.error('Error removing link:', error);
  }
}

// Clear all links
async function clearLinks() {
  try {
    const response = await fetch('http://localhost:3000/clearLinks', {
      method: 'DELETE',
    });

    const data = await response.json();
    if (data.success) {
      alert('All links cleared!');
      loadLinks();
    } else {
      alert('Failed to clear links');
    }
  } catch (error) {
    console.error('Error clearing links:', error);
  }
}
