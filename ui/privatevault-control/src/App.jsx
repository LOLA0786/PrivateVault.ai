import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Blog from './blog/Blog';
import BlogPost from './blog/BlogPost';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/blog" element={<Blog />} />
        <Route path="/blog/:slug" element={<BlogPost />} />
      </Routes>
    </BrowserRouter>
  );
}
