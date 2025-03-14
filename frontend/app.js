/**
 * Semantic Emoji Search Application
 * A web app for searching emojis using deep learning semantic understanding
 */

// API Configuration
// No need for full URL since we're serving from the same origin
const API_BASE_URL = '';

// API Endpoints
const API = {
  search: (query, topK = 20) => 
    `${API_BASE_URL}/api/emoji/search?query=${encodeURIComponent(query)}&top_k=${topK}`,
  getAllEmojis: () => `${API_BASE_URL}/api/emoji/all`,
  getEmojiGroups: () => `${API_BASE_URL}/api/emoji/groups`,
  getEmojisByGroup: (group) => `${API_BASE_URL}/api/emoji/group/${encodeURIComponent(group)}`,
};

// DOM Elements
const elements = {
  searchForm: document.getElementById('search-form'),
  searchInput: document.getElementById('search-input'),
  loadingIndicator: document.getElementById('loading-indicator'),
  clearButton: document.getElementById('clear-button'),
  searchPrompt: document.getElementById('search-prompt'),
  noResults: document.getElementById('no-results'),
  noResultsQuery: document.getElementById('no-results-query'),
  resultsContainer: document.getElementById('results-container'),
  resultsCount: document.getElementById('results-count'),
  emojiGrid: document.getElementById('emoji-grid'),
  emojiCardTemplate: document.getElementById('emoji-card-template'),
  copySuccessTemplate: document.getElementById('copy-success-template'),
  notificationToast: document.getElementById('notification-toast'),
  toastMessage: document.getElementById('toast-message'),
  currentYear: document.getElementById('current-year'),
};

// Bootstrap Toast instance
const toast = new bootstrap.Toast(elements.notificationToast);

// Initialize the app
function initApp() {
  // Set current year in footer
  elements.currentYear.textContent = new Date().getFullYear();
  
  // Add event listeners
  setupEventListeners();
}

// Set up all event listeners
function setupEventListeners() {
  // Search form submission
  elements.searchForm.addEventListener('submit', handleSearch);
  
  // Input field changes
  elements.searchInput.addEventListener('input', handleInputChange);
  
  // Clear button
  elements.clearButton.addEventListener('click', clearSearch);
}

// Handle search form submission
async function handleSearch(event) {
  event.preventDefault();
  
  const query = elements.searchInput.value.trim();
  
  if (!query) {
    clearSearch();
    return;
  }
  
  try {
    setLoading(true);
    
    const response = await fetch(API.search(query));
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    displayResults(data.results, query);
  } catch (error) {
    console.error('Search error:', error);
    showError('Failed to search emojis. Please try again.');
  } finally {
    setLoading(false);
  }
}

// Handle input field changes
function handleInputChange() {
  const hasValue = elements.searchInput.value.trim() !== '';
  
  if (hasValue) {
    elements.clearButton.classList.remove('d-none');
  } else {
    elements.clearButton.classList.add('d-none');
  }
}

// Clear search and reset UI
function clearSearch() {
  elements.searchInput.value = '';
  elements.clearButton.classList.add('d-none');
  
  // Reset UI state
  elements.searchPrompt.classList.remove('d-none');
  elements.noResults.classList.add('d-none');
  elements.resultsContainer.classList.add('d-none');
  
  // Clear results grid
  elements.emojiGrid.innerHTML = '';
}

// Set loading state
function setLoading(isLoading) {
  if (isLoading) {
    elements.loadingIndicator.classList.remove('d-none');
    elements.searchInput.setAttribute('disabled', 'true');
  } else {
    elements.loadingIndicator.classList.add('d-none');
    elements.searchInput.removeAttribute('disabled');
  }
}

// Display search results
function displayResults(results, query) {
  // Clear existing results
  elements.emojiGrid.innerHTML = '';
  
  // Hide search prompt
  elements.searchPrompt.classList.add('d-none');
  
  if (results.length === 0) {
    // Show no results message
    elements.noResults.classList.remove('d-none');
    elements.noResultsQuery.textContent = query;
    elements.resultsContainer.classList.add('d-none');
  } else {
    // Hide no results message
    elements.noResults.classList.add('d-none');
    
    // Update results count
    elements.resultsCount.textContent = `${results.length} ${results.length === 1 ? 'result' : 'results'} for "${query}"`;
    
    // Show results container
    elements.resultsContainer.classList.remove('d-none');
    
    // Add each emoji result to the grid
    results.forEach((emoji, index) => {
      const emojiElement = createEmojiElement(emoji, index);
      elements.emojiGrid.appendChild(emojiElement);
    });
  }
}

// Create emoji card element
function createEmojiElement(emoji, index) {
  // Clone the template
  const template = elements.emojiCardTemplate.content.cloneNode(true);
  const emojiCard = template.querySelector('.emoji-card');
  
  // Set emoji data
  const emojiDisplay = template.querySelector('.emoji-display');
  emojiDisplay.textContent = emoji.emoji;
  
  const emojiName = template.querySelector('.emoji-name');
  emojiName.textContent = emoji.name;
  
  const groupBadge = template.querySelector('.group-badge');
  groupBadge.textContent = emoji.group;
  
  const scoreBadge = template.querySelector('.score-badge');
  if (emoji.score) {
    scoreBadge.textContent = `${Math.round(emoji.score * 100)}%`;
  } else {
    scoreBadge.classList.add('d-none');
  }
  
  // Add click handler to copy emoji
  emojiCard.addEventListener('click', () => copyEmojiToClipboard(emoji.emoji, emojiCard));
  
  // Add animation delay based on index
  const column = template.querySelector('.col');
  column.style.animationDelay = `${index * 50}ms`;
  column.classList.add('animate-in');
  
  return template;
}

// Copy emoji to clipboard
async function copyEmojiToClipboard(emoji, cardElement) {
  try {
    // Try to use Clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(emoji);
      showCopySuccess(cardElement);
      return;
    }
    
    // Fallback method for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = emoji;
    textArea.style.position = 'fixed';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    const successful = document.execCommand('copy');
    document.body.removeChild(textArea);
    
    if (successful) {
      showCopySuccess(cardElement);
    } else {
      throw new Error('Copy command failed');
    }
  } catch (error) {
    console.error('Failed to copy emoji:', error);
    showError('Failed to copy emoji to clipboard');
  }
}

// Show copy success animation
function showCopySuccess(cardElement) {
  // Clone the success overlay template
  const successTemplate = elements.copySuccessTemplate.querySelector('.copy-success-overlay').cloneNode(true);
  
  // Add to card
  cardElement.appendChild(successTemplate);
  
  // Remove after animation
  setTimeout(() => {
    successTemplate.classList.add('fade-out');
    setTimeout(() => {
      cardElement.removeChild(successTemplate);
    }, 200);
  }, 1500);
}

// Show error toast notification
function showError(message) {
  elements.toastMessage.textContent = message;
  toast.show();
}

// Initialize the app when DOM is fully loaded
document.addEventListener('DOMContentLoaded', initApp); 