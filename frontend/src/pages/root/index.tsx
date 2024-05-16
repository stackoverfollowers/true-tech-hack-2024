import { useGetEvents } from '@entities/event/api';
import { Container, Fab, Typography, styled } from '@mui/material';
import { LiveEvent } from '@widgets/live-event';

import AddIcon from '@mui/icons-material/Add';
import { useState } from 'react';
import { CreatePlaceModal } from '@widgets/create-place-modal';

const Title = styled(Typography)({
  fontSize: '2rem',
  fontWeight: '600',
});

const StyledContainer = styled(Container)({
  position: 'relative',
  padding: 10,
});

const Cards = styled('div')(() => ({
  display: 'flex',
  flexWrap: 'wrap',
  margin: '0 -8px',
}));

const Wrapper = styled('div')(({ theme }) => ({
  position: 'relative',
  marginTop: theme.spacing(3),
  width: '100%',
  minHeight: '1px',
  paddingInline: theme.spacing(1),
  flex: '0 0 100%',
  maxWidth: '100%',

  [theme.breakpoints.up('sm')]: {
    flex: '0 0 50%',
    maxWidth: '50%',
  },

  [theme.breakpoints.up('md')]: {
    flex: '0 0 33.333333%',
    maxWidth: '33.333333%',
  },
}));

const StyledFab = styled(Fab)({
  position: 'absolute',
  bottom: 2,
  right: 2,
});

export const RootPage = () => {
  const { data } = useGetEvents();

  const [open, setOpen] = useState(false);

  return (
    <>
      <StyledContainer>
        <Title variant="h2">Афиша Санкт-Петербурга</Title>
      </StyledContainer>
      <StyledContainer>
        <Cards>
          {data?.items.map((item, idx) => (
            <Wrapper key={idx}>
              <LiveEvent {...item} />
            </Wrapper>
          ))}
        </Cards>
        <StyledFab color="primary" onClick={() => setOpen(true)}>
          <AddIcon />
        </StyledFab>
        <CreatePlaceModal open={open} onClose={() => setOpen(false)} />
      </StyledContainer>
    </>
  );
};
