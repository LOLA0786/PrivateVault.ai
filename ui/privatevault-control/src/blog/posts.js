const files = import.meta.glob('./posts/*.md', { eager: true, query: '?raw', import: 'default' });
function parseFrontmatter(raw) {
  const m = raw.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
  if (!m) return { data: {}, body: raw };
  const data = {};
  m[1].split('\n').forEach((line) => {
    const i = line.indexOf(':');
    if (i === -1) return;
    let v = line.slice(i + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    data[line.slice(0, i).trim()] = v;
  });
  return { data, body: m[2] };
}
export const posts = Object.entries(files)
  .map(([path, raw]) => {
    const { data, body } = parseFrontmatter(raw);
    const file = path.split('/').pop().replace(/\.md$/, '');
    const slug = data.slug || file.replace(/^\d{4}-\d{2}-\d{2}-/, '');
    return { slug, title: data.title || slug, date: data.date || '', excerpt: data.excerpt || '', body };
  })
  .sort((a, b) => new Date(b.date) - new Date(a.date));
export const getPost = (slug) => posts.find((p) => p.slug === slug);
