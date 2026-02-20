const fs = require('fs');
const path = require('path');

async function main() {
  try {
    const portfolioContent = await getPortfolioUpdates();
    const headerContent = await generateHeader();

    const readmePath = path.join(__dirname, '..', 'README.md');
    let readme = fs.readFileSync(readmePath, 'utf8');
    const originalReadme = readme;

    // Update Header
    readme = readme.replace(
      /<!-- HEADER_START -->[\s\S]*?<!-- HEADER_END -->/,
      `<!-- HEADER_START -->\n${headerContent}\n<!-- HEADER_END -->`
    );

    // Update Portfolio section
    console.log('Generating Portfolio Content...');
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

async function generateHeader() {
  const photoUrl = await getLatestPhoto();

  return `
<table width="100%">
  <tr>
    <td valign="top" width="25%">
      <h3>Who I Am</h3>
      <p>I'm <b>Gabriel 👋</b>, currently working as a <b>Researcher</b> and focusing on my <b>Master's degree</b>.</p>
    </td>
    <td valign="top" width="25%">
      <h3>What I Do</h3>
      <p>I focus on <b>personal projects</b> and exploring the entrepreneurial world with a <b>company</b> and a <b>micro SaaS</b>.</p>
    </td>
    <td valign="center" width="25%" align="center">
      <img src="${photoUrl}" alt="Latest Photo" width="100%" style="border-radius: 10px;" />
      <br />
      <sub>Latest Photo from Blog</sub>
    </td>
    <td valign="top" width="25%" align="center">
      <h3>Let's Connect</h3>
      <a href="https://a-new-type-portifolio.vercel.app/">
        <img src="https://img.shields.io/badge/Blog-2ea44f?style=for-the-badge&logo=rss" height="28" />
      </a>
      <br/>
      <a href="https://www.linkedin.com/in/gabriel-nascimento-gama-5b0b30185/">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="28" />
      </a>
      <br/>
      <a href="https://x.com/uMagicalJake">
        <img src="https://img.shields.io/badge/Twitter-000000?style=for-the-badge&logo=x&logoColor=white" height="28" />
      </a>
      <br/>
      <a href="mailto:gabrielngama@gmail.com">
        <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" height="28" />
      </a>
    </td>
  </tr>
</table>
  `;
}

async function getLatestPhoto() {
  try {
    const res = await fetch('https://a-new-type-portifolio.vercel.app/api/photos');
    const json = await res.json();
    if (json.success && json.data && json.data.length > 0) {
      // Sort by date desc
      const sorted = json.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      return sorted[0].image_url;
    }
  } catch (e) {
    console.error('Error fetching photos:', e);
  }
  // Fallback
  return 'https://via.placeholder.com/400x300?text=No+Photo+Found';
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
        url = `https://a-new-type-portifolio.vercel.app/${item.link}`;
      }

      return {
        ...item,
        sourceType: type,
        emoji: emoji,
        url: url,
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
  items = items.sort((a, b) => {
    const dateA = new Date(a.created_at || a.date);
    const dateB = new Date(b.created_at || b.date);
    return dateB - dateA;
  });

  // Generate History File
  const grouped = {};
  items.forEach(item => {
    const date = new Date(item.created_at);
    const monthYear = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' })
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
      let type = post.tag || post.sourceType;
      historyContent += `- [${post.title}](${post.url}) - ${date} • **${type}**\n`;
    });
    historyContent += `\n`;
  }

  try {
    fs.writeFileSync(path.join(__dirname, '..', 'BLOG_HISTORY.md'), historyContent);
  } catch (e) { }

  // Limit to 5 for README (Original constraint)
  const topItems = items.slice(0, 5);

  let listHtml = '<ul>\n';
  listHtml += topItems.map(item => {
    const date = formatDate(item.created_at);
    let tag = item.tag || item.sourceType;

    // Use English title if available
    const title = item.title_en || item.title;

    let color = '0077b5'; // Default Blue
    const lowerTag = (tag || '').toLowerCase();

    if (lowerTag.includes('leetcode')) color = 'FF69B4'; // Pink
    else if (lowerTag.includes('review') || lowerTag.includes('book')) color = '800080'; // Purple
    else if (lowerTag.includes('study') || lowerTag.includes('note')) color = 'ADD8E6'; // Light Blue
    else if (lowerTag.includes('guide') || lowerTag.includes('tutorial')) color = 'FFA500'; // Orange
    else if (lowerTag.includes('photo')) color = '008000'; // Green
    else if (lowerTag.includes('thoughts')) color = '0077b5'; // Blue

    const safeTag = encodeURIComponent(tag);
    const tagBadge = `<img src="https://img.shields.io/badge/${safeTag}-${color}?style=flat-square" height="20"/>`;

    return `<li><a href="${item.url}" target="_blank">${title}</a> - ${date} • ${tagBadge}</li>`;
  }).join('\n'); // No extra newlines in join to be consistent with original style if needed

  listHtml += `\n<br/>\n<li><a href="BLOG_HISTORY.md">... See all old posts</a></li>\n</ul>`;

  return listHtml;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toISOString().split('T')[0];
}


// Run main
main();
