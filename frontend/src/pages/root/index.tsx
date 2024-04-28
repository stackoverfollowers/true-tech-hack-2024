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
  return (
    <>
      <StyledContainer>
        <Title variant="h2">Афиша Санкт-Петербурга</Title>
      </StyledContainer>
      <StyledContainer>
        <Cards>
          {[...Array(30)].map((_, idx) => (
            <Wrapper key={idx}>
              <LiveEvent
                id={idx}
                img="https://live.mts.ru/image/536x360/affinazh-russkie-pesni-s-orkestrom-narodnykh-instrumentov-09321d6d-b516-086e-12c3-1c87ef582f53.jpg"
                title="Концерт «Mary Gu. Club Show»"
                time="12 мая, 18:00"
                place="Гигант-Холл"
                price="1000р"
                discount="10%"
                accessibilityType="Bad"
                accessibility="Недоступно для инвалидов"
              />
            </Wrapper>
          ))}
        </Cards>
      </StyledContainer>
    </>
  );
};
