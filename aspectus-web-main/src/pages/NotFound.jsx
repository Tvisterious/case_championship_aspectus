import { Box, Typography } from "@mui/material"
import '../styles.css'
import { useNavigate } from "react-router-dom"
import { ButtonClick } from "../components/ButtonClick"

function NotFound() {
  const navigate = useNavigate()

  return(
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
    >
        <Typography 
          variant="h1" 
          color="var(--orange-primary)"
          sx={{ fontWeight: 500 }}
        >
            404
        </Typography>
        <Typography variant="h4" >
            Упс! Кажется, что такой страницы не существует.
        </Typography>
        <ButtonClick
            label="На главную"
            onClick={() => navigate("/enterData")}
            color="var(--orange-primary)"
            colorHover="var(--orange-secondary)"
            colorText="white"
        />
    </Box>  
  )
}

export default NotFound