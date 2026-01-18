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

  const posts = data
    .filter(item => item.parent_id === null && item.title) // Top level posts only
    .slice(0, 5); // Limit to 5

  return posts.map(post => {
    const date = formatDate(post.published_at);
    const isNew = isRecent(post.published_at);
    const badge = isNew ? ' <img src="https://img.shields.io/badge/New-red?style=flat-square" height="15"/>' : '';
    return `<li><a href="https://www.tabnews.com.br/${post.owner_username}/${post.slug}" target="_blank">${post.title}</a> - ${date} ${badge}</li>`;
  }).join('\n');
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
  items = items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 5);

  return items.map(item => {
    const date = formatDate(item.created_at);
    // Use tag if available, otherwise sourceType
    let tag = item.tag || item.sourceType;
    // Map specific tags to badges/colors if needed, or just text
    const tagBadge = `<b>${item.emoji} ${tag}</b>`; 
    
    return `<li><a href="${item.url}" target="_blank">${item.title}</a> - ${date} • ${tagBadge}</li>`;
  }).join('\n');
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
