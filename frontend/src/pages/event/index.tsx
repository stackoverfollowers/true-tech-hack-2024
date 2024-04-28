import { Chip, Container, Stack, Typography, styled } from '@mui/material';
import { Event } from '@shared/types/events';
import { AccessibilityChip } from '@widgets/accessibility-chip';

const data: Event = {
  title: 'Аффинаж. Русские песни с оркестром народных инструментов',
  img: 'https://live.mts.ru/image/536x360/affinazh-russkie-pesni-s-orkestrom-narodnykh-instrumentov-09321d6d-b516-086e-12c3-1c87ef582f53.jpg',
  place: 'МТС Live Холл Санкт-Петербург',
  rating: '16+',
  accessibility: 'Недоступно',
};

const StyledImg = styled('img')({
  objectFit: 'contain',
  width: '30rem',
  borderRadius: 16,
});

const StyledChip = styled(Chip)({
  width: 'max-content',
});

const StyledGrid = styled('div')({
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
});

const Labels = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  columnGap: 5,
});

const StyledTitle = styled('h1')({
  fontSize: 30,
  m: 0,
});

export const EventPage = () => {
  const { accessibility, img, place, rating, title } = data;
  return (
    <Container>
      <StyledGrid>
        <StyledImg src={img}></StyledImg>
        <Stack>
          <StyledTitle>{title}</StyledTitle>
          <Typography variant="h6">{place}</Typography>
          <Labels>
            <StyledChip label={rating} />
            <AccessibilityChip ac="Bad" label={accessibility} />
          </Labels>
        </Stack>
      </StyledGrid>
    </Container>
  );
};
