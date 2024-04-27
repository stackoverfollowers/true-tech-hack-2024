import { Box, Container } from '@mui/material';
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
        <Container
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            pt: { xs: 14, sm: 20 },
            pb: { xs: 8, sm: 12 },
          }}
        >
          <Outlet />
        </Container>
      </Box>
    </>
  );
};
