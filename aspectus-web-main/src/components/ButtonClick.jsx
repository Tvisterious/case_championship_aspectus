import { Button } from "@mui/material";

export const ButtonClick = ({ label, onClick, type, color, colorHover, colorText, disabled = false }) => {
  return (
    <Button
      type={type}
      onClick={onClick}
      fullWidth
      variant="contained"
      disabled={disabled}
      sx={{
        backgroundColor: color,
        color: colorText,
        borderRadius: "24px",
        textTransform: "none",
        minWidth: "154px",
        width: "258px",
        height: "48px",
        py: "12px",
        px: "32px",
        mb: 1,
        mt: 2, 
        gap: "8px",
        fontWeight: "bold",
        ":hover": { backgroundColor: colorHover },
      }}
    >
      {label}
    </Button>
  );
};