import { useState } from "react";
import { Box, TextField, Typography, MenuItem } from "@mui/material";

export const InputField = ({
  label,
  placeholder,
  type,
  register,
  error,
  options
}) => {
  const [labelVisible, setLabelVisible] = useState(true);

  const textFieldStyles = {
    "& .MuiOutlinedInput-root": {
      borderRadius: "24px",
      backgroundColor: "var(--milky-primary)",
      width: "100%",
      "& fieldset": { border: "none" },
      "&.Mui-disabled": {
        opacity: 1
      },
      "&.Mui-disabled input": {
        color: "black",
        WebkitTextFillColor: "black"
      },
    },
    "& input[type='date']::-webkit-calendar-picker-indicator": {
      filter: "invert(0%)",
      cursor: "pointer"
    },
    "& input[type='date']": {
      colorScheme: "light",
    },
    // Кастомизация MenuItem внутри Select
    "& .MuiSelect-select": {
      cursor: "pointer"
    },
    "& .MuiMenu-paper": {
      borderRadius: "16px",
    },
    "& .MuiMenuItem-root": {
      borderRadius: "12px",
      "&:hover": {
        backgroundColor: "var(--orange-primary-light)", // можно свой цвет
      }
    }
  };

  return (
    <>
      <Typography align="left" sx={{ mb: -2 }}>
        {label}
      </Typography>
      <Box sx={{ position: "relative", display: "flex", alignItems: "center" }}>
        <TextField
          {...register}
          fullWidth
          label={labelVisible ? placeholder : ""}
          type={type}
          size="small"
          variant="outlined"
          margin="normal"
          onFocus={() => setLabelVisible(false)}
          onBlur={(e) => setLabelVisible(e.target.value === "")}
          onInput={(e) => setLabelVisible(e.target.value === "")}
          sx={textFieldStyles}
          error={!!error}
          helperText={error?.message || ""}
          select={!!options}
        >
          {options &&
            options.map((opt) => (
              <MenuItem key={opt} value={opt}>
                {opt}
              </MenuItem>
            ))}
        </TextField>
      </Box>
    </>
  );
};