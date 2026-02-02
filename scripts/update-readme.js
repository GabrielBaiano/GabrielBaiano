const fs = require('fs');
const path = require('path');

async function main() {
  try {
    const tabNewsContent = await getTabNews();
    const portfolioContent = await getPortfolioUpdates();
    const headerContent = await generateHeader();
    const booksContent = await getBooks();

    const readmePath = path.join(__dirname, '..', 'README.md');
    let readme = fs.readFileSync(readmePath, 'utf8');
    const originalReadme = readme;

    // Update Header
    readme = readme.replace(
      /<!-- HEADER_START -->[\s\S]*?<!-- HEADER_END -->/,
      `<!-- HEADER_START -->\n${headerContent}\n<!-- HEADER_END -->`
    );

    // Update Books section
    readme = readme.replace(
      /<!-- BOOKS_START -->[\s\S]*?<!-- BOOKS_END -->/,
      `<!-- BOOKS_START -->\n${booksContent}\n<!-- BOOKS_END -->`
    );

    // Update TabNews section
    readme = readme.replace(
      /<!-- TABNEWS_START -->[\s\S]*?<!-- TABNEWS_END -->/,
      `<!-- TABNEWS_START -->\n${tabNewsContent}\n<!-- TABNEWS_END -->`
    );

    // Update Portfolio section
    console.log('Generating Portfolio Content...');
    const oldReadmeLen = readme.length;
    readme = readme.replace(
      /<!-- PORTFOLIO_START -->[\s\S]*?<!-- PORTFOLIO_END -->/,
      `<!-- PORTFOLIO_START -->\n${portfolioContent}\n<!-- PORTFOLIO_END -->`
    );

    if (readme === originalReadme) {
      console.warn('WARNING: Portfolio section was NOT updated (content same).');
      const regex = /<!-- PORTFOLIO_START -->[\s\S]*?<!-- PORTFOLIO_END -->/;
      const match = readme.match(regex);
      if (match) {
        console.log('EXISTING BLOCK (first 200 chars):', match[0].substring(0, 200));
        console.log('NEW ENTRY (first 200 chars):', `<!-- PORTFOLIO_START -->\n${portfolioContent}\n<!-- PORTFOLIO_END -->`.substring(0, 200));
      }
    } else {
      console.log('Portfolio section updated. New items inserted.');
    }

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
<table>
  <tr>
    <td valign="top" width="50%">
      <h2>Hi there, I'm Gabriel 👋</h2>
      <p>Currently working as a <b>Researcher</b> and focusing on my <b>Master's degree</b>. In my free time, I focus on <b>personal projects</b> and exploring the entrepreneurial world with a <b>company</b> and a <b>micro SaaS</b>.</p>
      <br/>
      <a href="https://a-new-type-portifolio.vercel.app/">
        <img src="https://img.shields.io/badge/Visit_my_Blog-2ea44f?style=for-the-badge&logo=rss" height="30" />
      </a>
      <a href="https://www.linkedin.com/in/gabriel-nascimento-gama-5b0b30185/">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="30" />
      </a>
      <br/>
      <br/>
      <a href="https://x.com/uMagicalJake">
        <img src="https://img.shields.io/badge/Twitter-000000?style=for-the-badge&logo=x&logoColor=white" height="30" />
      </a>
      <a href="mailto:gabrielngama@gmail.com">
        <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" height="30" />
      </a>
    </td>
    <td valign="center" width="50%" align="center">
      <img src="${photoUrl}" alt="Latest Photo" width="100%" style="border-radius: 10px;" />
      <br/>
      <sub>Latest Photo from Blog</sub>
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
  // Fallback if no photo found or error
  return 'https://via.placeholder.com/400x300?text=No+Photo+Found';
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
    // Format: "JANUARY 2026"
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
  console.log('Top 5 items to carry to README:');
  topItems.forEach((item, i) => console.log(`${i + 1}. ${item.title} (${item.created_at})`));

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

async function getBooks() {
  let currentlyReadingHtml = '';
  let booksReadCount = 0;
  const currentYear = new Date().getFullYear();

  try {
    // 1. Get Currently Reading from README
    const readmeRes = await fetch('https://raw.githubusercontent.com/GabrielBaiano/personal-library/main/README.md');
    const readmeText = await readmeRes.text();

    // Extract the "Reading" table
    const tableMatch = readmeText.match(/<table>[\s\S]*?Reading[\s\S]*?<\/table>/);
    if (tableMatch) {
      currentlyReadingHtml = tableMatch[0];
      // "Decentralize" (move to left/standard flow) by removing the center wrapper
    } else {
      currentlyReadingHtml = '<p>Not reading anything public right now.</p>';
    }

    // 2. Get Books Read Count from API (Folder count)
    // Using GitHub API to list content of the year folder
    const apiRes = await fetch(`https://api.github.com/repos/GabrielBaiano/personal-library/contents/${currentYear}`);
    if (apiRes.ok) {
      const files = await apiRes.json();
      if (Array.isArray(files)) {
        booksReadCount = files.length;
      }
    }

  } catch (error) {
    console.error('Error fetching books:', error);
    currentlyReadingHtml = 'Could not load books data.';
  }

  return `
<p>
  This is part of my <b><a href="https://github.com/GabrielBaiano/personal-library">Personal Library</a></b> project — a dedicated space where I organize my readings, share reflections, and build a consistent reading habit.
</p>

${currentlyReadingHtml}

<br/>

**${currentYear} Reading Progress:** ${booksReadCount} books read so far 🏁
<br/>
<a href="https://github.com/GabrielBaiano/personal-library">Check out my specific notes here!</a>
`;
}

// Run main
main();
