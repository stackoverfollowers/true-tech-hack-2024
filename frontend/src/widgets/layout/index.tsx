import { Box } from '@mui/material';
import { Header } from '@widgets/header';
import { Outlet } from 'react-router-dom';

export const Layout = () => {
  return (
    <>
      <Header />
      <Box
        sx={{
          width: '100%',
        }}
      >
        <Outlet />
      </Box>
    </>
  );
};
