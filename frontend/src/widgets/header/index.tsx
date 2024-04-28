import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import MenuItem from '@mui/material/MenuItem';
import { styled } from '@mui/material';
import { Link } from 'react-router-dom';

const logoStyle = {
  width: '140px',
  height: 'auto',
  cursor: 'pointer',
  padding: 5,
};

const StyledHeader = styled('header')({
  bgcolor: 'white',
  backgroundImage: 'none',
  mt: 2,
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
});

export const Header = () => {
  return (
    <StyledHeader>
      <Box
        sx={{
          flexGrow: 1,
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          p: 5,
        }}
      >
        <Link to="/">
          <img
            src={'https://live.mts.ru/images/header/Logo.svg'}
            style={logoStyle}
            alt="logo of mts"
          />
        </Link>
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          <MenuItem sx={{ py: '6px', px: '12px' }}>
            <Typography variant="h6" color="text.primary">
              Все события
            </Typography>
          </MenuItem>
          <MenuItem sx={{ py: '6px', px: '12px' }}>
            <Typography variant="h6" color="text.primary">
              Концерты
            </Typography>
          </MenuItem>
          <MenuItem sx={{ py: '6px', px: '12px' }}>
            <Typography variant="h6" color="text.primary">
              Театры
            </Typography>
          </MenuItem>
          <MenuItem sx={{ py: '6px', px: '12px' }}>
            <Typography variant="h6" color="text.primary">
              Мюзиклы
            </Typography>
          </MenuItem>
          <MenuItem sx={{ py: '6px', px: '12px' }}>
            <Typography variant="h6" color="text.primary">
              Стэндап
            </Typography>
          </MenuItem>
        </Box>
      </Box>
    </StyledHeader>
  );
};
