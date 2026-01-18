const fs = require('fs');
const path = require('path');

async function main() {
  try {
    const tabNewsContent = await getTabNews();
    const portfolioContent = await getPortfolioUpdates();

    const readmePath = path.join(__dirname, '..', 'README.md');
    let readme = fs.readFileSync(readmePath, 'utf8');

    // Update TabNews section
    readme = readme.replace(
      /<!-- TABNEWS_START -->[\s\S]*?<!-- TABNEWS_END -->/,
      `<!-- TABNEWS_START -->\n${tabNewsContent}\n<!-- TABNEWS_END -->`
    );

    // Update Portfolio section
    readme = readme.replace(
      /<!-- PORTFOLIO_START -->[\s\S]*?<!-- PORTFOLIO_END -->/,
      `<!-- PORTFOLIO_START -->\n${portfolioContent}\n<!-- PORTFOLIO_END -->`
    );

    fs.writeFileSync(readmePath, readme);
    console.log('README.md updated successfully!');
  } catch (error) {
    console.error('Error updating README:', error);
    process.exit(1);
  }
}

async function getTabNews() {
  const response = await fetch('https://www.tabnews.com.br/api/v1/contents/gabrielbaiano');
  const data = await response.json();

  const allPosts = data
    .filter(item => item.parent_id === null && item.title); // Top level posts only

  // Generate History File
  const historyContent = `# 📝 All TabNews Posts\n\n` + allPosts.map(post => {
    const date = formatDate(post.published_at);
    return `- [${post.title}](https://www.tabnews.com.br/${post.owner_username}/${post.slug}) - ${date}`;
  }).join('\n');
  
  fs.writeFileSync(path.join(__dirname, '..', 'TABNEWS_HISTORY.md'), historyContent);

  // Return Top 3 for README
  const topPosts = allPosts.slice(0, 3);
  
  let listHtml = topPosts.map(post => {
    const date = formatDate(post.published_at);
    const isNew = isRecent(post.published_at);
    const badge = isNew ? ' <img src="https://img.shields.io/badge/New-red?style=flat-square" height="15"/>' : '';
    // TabNews Badge removed as requested
    return `<li><a href="https://www.tabnews.com.br/${post.owner_username}/${post.slug}" target="_blank">${post.title}</a> - ${date} ${badge}</li>`;
  }).join('\n');

  // Add "More" link
  listHtml += `\n<br/>\n<li><a href="TABNEWS_HISTORY.md">... See all old posts</a></li>`;
  
  return listHtml;
}

async function getPortfolioUpdates() {
  // Parallel fetch
  const [feedRes, balloonsRes, photosRes] = await Promise.all([
    fetch('https://a-new-type-portifolio.vercel.app/api/feed'),
    fetch('https://a-new-type-portifolio.vercel.app/api/balloons?context=all'),
    fetch('https://a-new-type-portifolio.vercel.app/api/photos')
  ]);

  const feedData = await feedRes.json();
  const balloonsData = await balloonsRes.json();
  const photosData = await photosRes.json();

  let items = [];

  // 1. Feed (Thoughts/Manual)
  if (feedData.success && feedData.data) {
    items.push(...feedData.data.map(item => ({
      ...item,
      sourceType: 'Thoughts',
      emoji: '💭',
      url: `https://a-new-type-portifolio.vercel.app/#/detail/feed/${item.id}`
    })));
  }

  // 2. Balloons (Releases & LeetCode)
  if (balloonsData.success && balloonsData.data) {
    items.push(...balloonsData.data.map(item => {
      let type = 'Update';
      let emoji = '🚀';
      let url = item.link;

      if (item.type === 'leetcode') {
        type = 'LeetCode';
        emoji = '🧠';
        url = `https://a-new-type-portifolio.vercel.app/${item.link}`; // usually hash link
      }

      return {
        ...item,
        sourceType: type,
        emoji: emoji,
        url: url,
        // Normalize date
        created_at: item.date
      };
    }));
  }

  // 3. Photos
  if (photosData.success && photosData.data) {
    items.push(...photosData.data.map(item => ({
      ...item,
      title: item.description || 'New Photo',
      sourceType: 'Photo',
      emoji: '📸',
      url: 'https://a-new-type-portifolio.vercel.app/#/photos',
      created_at: item.created_at
    })));
  }

  // Sort by date desc
  items = items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

  // --- Generate History File (Grouped by Month) ---
  const grouped = {};
  items.forEach(item => {
    const date = new Date(item.created_at);
    // Format: "JANEIRO 2026"
    const monthYear = new Intl.DateTimeFormat('pt-BR', { month: 'long', year: 'numeric' })
      .format(date)
      .toUpperCase();
    
    if (!grouped[monthYear]) grouped[monthYear] = [];
    grouped[monthYear].push(item);
  });

  let historyContent = `# 🚀 All Blog Updates\n\n`;
  for (const [monthYear, posts] of Object.entries(grouped)) {
    historyContent += `### ${monthYear}\n\n`;
    posts.forEach(post => {
      const date = formatDate(post.created_at);
       // Determine Color for History (reuse logic or simplify)
       let type = post.tag || post.sourceType;
       historyContent += `- [${post.title}](${post.url}) - ${date} • **${type}**\n`;
    });
    historyContent += `\n`;
  }
  
  fs.writeFileSync(path.join(__dirname, '..', 'BLOG_HISTORY.md'), historyContent);
  // ------------------------------------------------

  // Limit to 5 for README
  const topItems = items.slice(0, 5);

  let listHtml = topItems.map(item => {
    const date = formatDate(item.created_at);
    // Use tag if available, otherwise sourceType
    let tag = item.tag || item.sourceType;
    
    // Determine Color
    let color = '0077b5'; // Default Blue
    const lowerTag = tag.toLowerCase();
    
    if (lowerTag.includes('leetcode')) color = 'FF69B4'; // Pink
    else if (lowerTag.includes('review') || lowerTag.includes('book')) color = '800080'; // Purple
    else if (lowerTag.includes('study') || lowerTag.includes('note')) color = 'ADD8E6'; // Light Blue
    else if (lowerTag.includes('guide') || lowerTag.includes('tutorial')) color = 'FFA500'; // Orange
    else if (lowerTag.includes('photo')) color = '008000'; // Green
    else if (lowerTag.includes('thoughts')) color = '0077b5'; // Blue

    // Badge
    // Encode tag for URL
    const safeTag = encodeURIComponent(tag);
    const tagBadge = `<img src="https://img.shields.io/badge/${safeTag}-${color}?style=flat-square" height="20"/>`;
    
    return `<li><a href="${item.url}" target="_blank">${item.title}</a> - ${date} • ${tagBadge}</li>`;
  }).join('\n');

  // Add "More" link for Blog Updates
  listHtml += `\n<br/>\n<li><a href="BLOG_HISTORY.md">... See all old posts</a></li>`;

  return listHtml;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toISOString().split('T')[0];
}

function isRecent(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays <= 14; 
}

main();
