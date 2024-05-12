import { useGetEvents } from '@entities/event/api';
import { Container, Typography, styled } from '@mui/material';
import { LiveEvent } from '@widgets/live-event';

const Title = styled(Typography)({
  fontSize: '2rem',
  fontWeight: '600',
});

const StyledContainer = styled(Container)({
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

export const RootPage = () => {
  const { data } = useGetEvents();

  console.log('data', data)

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
      </StyledContainer>
    </>
  );
};
