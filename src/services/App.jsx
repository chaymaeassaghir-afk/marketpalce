import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Catalogue from './pages/Catalogue';
import Dashboard from './pages/Dashboard';
import Paiement from './pages/Paiement';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/catalogue" element={<Catalogue />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/paiement" element={<Paiement />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
