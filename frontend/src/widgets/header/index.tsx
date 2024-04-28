import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import MenuItem from '@mui/material/MenuItem';
import { clsx } from 'clsx';
import { Link } from 'react-router-dom';

import styles from './styles.module.css';
import { useEffect, useState } from 'react';

const logoStyle = {
  width: '140px',
  height: 'auto',
  cursor: 'pointer',
  padding: 5,
};
export const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
      setIsScrolled(scrollPosition >= 100);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className={styles.root}>
      <header
        className={clsx(styles.header, {
          [styles.shadow]: isScrolled,
        })}
      >
        <Box
          sx={{
            flexGrow: 1,
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'center',
            p: 2,
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
      </header>
    </div>
  );
};
