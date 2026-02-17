const fs = require('fs');
const path = require('path');

async function main() {
  try {
    // 1. Fetch Data
    const portfolioContent = await getPortfolioUpdates();
    const headerContent = await generateHeader();
    const booksContent = await getBooks();
    const photoContent = await generatePhotoSection();

    const readmePath = path.join(__dirname, '..', 'README.md');
    let readme = fs.readFileSync(readmePath, 'utf8');
    const originalReadme = readme;

    // 2. Update Header
    readme = readme.replace(
      /<!-- HEADER_START -->[\s\S]*?<!-- HEADER_END -->/,
      `<!-- HEADER_START -->\n${headerContent}\n<!-- HEADER_END -->`
    );

    // 3. Update Books section
    readme = readme.replace(
      /<!-- BOOKS_START -->[\s\S]*?<!-- BOOKS_END -->/,
      `<!-- BOOKS_START -->\n${booksContent}\n<!-- BOOKS_END -->`
    );

    // 4. Update Portfolio section (Blog Updates)
    console.log('Generating Portfolio Content...');
    readme = readme.replace(
      /<!-- PORTFOLIO_START -->[\s\S]*?<!-- PORTFOLIO_END -->/,
      `<!-- PORTFOLIO_START -->\n${portfolioContent}\n<!-- PORTFOLIO_END -->`
    );

    // 5. Update Photo section
    readme = readme.replace(
      /<!-- PHOTO_START -->[\s\S]*?<!-- PHOTO_END -->/,
      `<!-- PHOTO_START -->\n${photoContent}\n<!-- PHOTO_END -->`
    );

    // 6. Save
    fs.writeFileSync(readmePath, readme);
    console.log('README.md updated successfully!');
  } catch (error) {
    console.error('Error updating README:', error);
    process.exit(1);
  }
}

async function generateHeader() {
  return `
<div align="left">
  <h2>Hi there, I'm Gabriel 👋</h2>
  <p>Currently working as a <b>Researcher</b> and focusing on my <b>Master's degree</b>. In my free time, I focus on <b>personal projects</b> and exploring the entrepreneurial world with a <b>company</b> and a <b>micro SaaS</b>.</p>
  <br/>
  <a href="https://a-new-type-portifolio.vercel.app/">
    <img src="https://img.shields.io/badge/Visit_my_Blog-2ea44f?style=for-the-badge&logo=rss" height="30" />
  </a>
  <a href="https://www.linkedin.com/in/gabriel-nascimento-gama-5b0b30185/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="30" />
  </a>
  <a href="https://x.com/uMagicalJake">
    <img src="https://img.shields.io/badge/Twitter-000000?style=for-the-badge&logo=x&logoColor=white" height="30" />
  </a>
  <a href="mailto:gabrielngama@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" height="30" />
  </a>
</div>
`;
}

async function generatePhotoSection() {
  const photoUrl = await getLatestPhoto();
  return `
<div align="center">
  <img src="${photoUrl}" alt="Latest Photo" width="100%" style="border-radius: 10px;" />
  <br/>
  <sub>Latest Photo from Blog</sub>
</div>
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

  // Generate History File (Optional: Keep or remove depending on preference, logic kept for now)
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
      const pDate = formatDate(post.created_at);
      let pType = post.tag || post.sourceType;
      historyContent += `- [${post.title}](${post.url}) - ${pDate} • **${pType}**\n`;
    });
    historyContent += `\n`;
  }
  try {
    fs.writeFileSync(path.join(__dirname, '..', 'BLOG_HISTORY.md'), historyContent);
  } catch (e) { }

  // Limit to 8 for Grid (Giving more space since it's a dedicated column)
  const topItems = items.slice(0, 8); // Display more items

  let listHtml = '<ul>\n';
  listHtml += topItems.map(item => {
    const date = formatDate(item.created_at);
    // Use tag if available, otherwise sourceType
    let tag = item.tag || item.sourceType;

    // Determine Color
    let color = '0077b5'; // Default Blue
    const lowerTag = (tag || '').toLowerCase();

    if (lowerTag.includes('leetcode')) color = 'FF69B4'; // Pink
    else if (lowerTag.includes('review') || lowerTag.includes('book')) color = '800080'; // Purple
    else if (lowerTag.includes('study') || lowerTag.includes('note')) color = 'ADD8E6'; // Light Blue
    else if (lowerTag.includes('guide') || lowerTag.includes('tutorial')) color = 'FFA500'; // Orange
    else if (lowerTag.includes('photo')) color = '008000'; // Green
    else if (lowerTag.includes('thoughts')) color = '0077b5'; // Blue
    else if (lowerTag.includes('tabnews')) color = '0ea5e9'; // TabNews Blue

    // Badge
    const safeTag = encodeURIComponent(tag);
    const tagBadge = `<img src="https://img.shields.io/badge/${safeTag}-${color}?style=flat-square" height="20"/>`;

    return `<li><a href="${item.url}" target="_blank">${item.title}</a> - ${date} • ${tagBadge}</li>`;
  }).join('\n');

  listHtml += `\n<br/>\n<li><a href="BLOG_HISTORY.md">... See all old posts</a></li>\n</ul>`;

  return listHtml;
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toISOString().split('T')[0];
}

async function getBooks() {
  let booksHtml = '';
  // Start the list container
  booksHtml += '<ul>\n';

  // 1. Get Currently Reading from README (for descriptions/images)
  try {
    const readmeRes = await fetch('https://raw.githubusercontent.com/GabrielBaiano/personal-library/main/README.md');
    const readmeText = await readmeRes.text();

    // Regex to find books in the table
    // Looking for: <a href="(google_book_link)">...<img src="(img_src)">...<b>(Title)</b>...Status: <b>Reading</b>
    // This is brittle but works for the current format.

    // Simpler extraction strategy:
    // Split by <td>...</td>
    const cells = readmeText.match(/<td align="center">[\s\S]*?<\/td>/g);

    if (cells && cells.length > 0) {
      cells.forEach(cell => {
        // Extract details
        const imgMatch = cell.match(/src="([^"]+)"/);
        const titleMatch = cell.match(/<b>(.*?)<\/b>/); // Title inside <b>
        const linkMatch = cell.match(/href="([^"]+)"/); // First href
        // const statusMatch = cell.match(/Status: <b>(.*?)<\/b>/);

        if (titleMatch && imgMatch) {
          const title = titleMatch[1];
          const img = imgMatch[1];
          const link = linkMatch ? linkMatch[1] : '#';

          // Create Detail Item
          booksHtml += `
  <li style="list-style-type: none; margin-bottom: 10px;">
    <details>
      <summary><b>${title}</b> - <a href="${link}">View Book</a></summary>
      <br/>
      <div align="center">
        <img src="${img}" alt="${title}" width="100">
        <br/>
        <p><i>Click the link above to see highlights and notes.</i></p>
      </div>
    </details>
  </li>`;
        }
      });
    } else {
      booksHtml += '<li>No books currently being read.</li>';
    }

  } catch (error) {
    console.error('Error fetching books:', error);
    booksHtml += '<li>Could not load books data.</li>';
  }

  booksHtml += '\n</ul>';

  // Footer for Books
  booksHtml += `
<br/>
<a href="https://github.com/GabrielBaiano/personal-library">Check out my specific notes here!</a>`;

  return booksHtml;
}

// Run main
main();
