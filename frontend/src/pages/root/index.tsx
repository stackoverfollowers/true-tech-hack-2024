import { Container, Grid, Typography, styled } from '@mui/material';
import { LiveEvent } from '@widgets/live-event';

const Title = styled(Typography)({
  fontSize: '2rem',
  fontWeight: '600',
});

const StyledContainer = styled(Container)({
  padding: 10,
});

export const RootPage = () => {
  return (
    <>
      <StyledContainer>
        <Title variant="h2">Афиша Санкт-Петербурга</Title>
      </StyledContainer>
      <StyledContainer>
        <Grid container rowSpacing={1} columnSpacing={{ xs: 6, sm: 12, md: 18 }}>
          {Array(100)
            .fill(undefined)
            .map(() => (
              <Grid item xs={4} sx={{ alignItems: 'center' }}>
                <LiveEvent
                  id="1"
                  img="https://live.mts.ru/image/536x360/affinazh-russkie-pesni-s-orkestrom-narodnykh-instrumentov-09321d6d-b516-086e-12c3-1c87ef582f53.jpg"
                  title="Концерт «Mary Gu. Club Show»"
                  time="12 мая, 18:00"
                  place="Гигант-Холл"
                  price="1000р"
                  discount="10%"
                  accessibilityType="Bad"
                  accessibility="Недоступно для инвалидов"
                />
              </Grid>
            ))}
        </Grid>
      </StyledContainer>
    </>
  );
};
