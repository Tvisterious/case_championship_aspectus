import './styles.css'
import { Container } from '@mui/material'
import { Route, Routes } from 'react-router-dom'
import MainForm from './pages/mainForm'
import NotFound from './pages/NotFound'

function App() {

  return (
    <>
      <Container sx = {{justifyContent: 'center', color: 'black'}}>
        <Routes>
          <Route path="/enterData" element={<MainForm/>} />
          <Route path="/" element={<MainForm/>} />
          <Route path='*' element={<NotFound />} />
        </Routes>  
      </Container> 
    </>
  )
}

export default App
