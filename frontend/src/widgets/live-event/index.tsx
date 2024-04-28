import { Box, Typography, styled, Chip, Stack, Paper } from '@mui/material';
import { Accessibility } from '@shared/types/accessibility';
import { AccessibilityChip } from '@widgets/accessibility-chip';
import { Link } from 'react-router-dom';

const StyledBox = styled(Box)({
  backgroundColor: 'transparent',
  width: '25rem',
});

const StyledPaper = styled(Paper)({
  padding: 20,
  borderRadius: 16,
  display: 'flex',
  flexDirection: 'column',
  rowGap: 20,
});

const StyledImg = styled('img')({
  borderRadius: 16,
  objectFit: 'contain',
  objectPosition: '50% 50%',
  width: '100%',
  height: '100%',
  overflowClipMargin: 'content-box',
  transform: 'matrix(1, 0, 0, 1, 0, 0)',
});

const ColoredChip = styled(Chip)({
  backgroundColor: '#7C86FE',
  color: 'white',
  fontSize: 12,
  fontWeight: 500,
});

const GrayChip = styled(Chip)({
  backgroundColor: '#F2F3F7',
  color: 'black',
  fontWeight: 500,
  fontSize: 12,
});

const Labels = styled('div')({
  columnGap: 10,
  display: 'flex',
});

type LiveEventProps = {
  id: string;
  img: string;
  title: string;
  price: string;
  discount: string;
  accessibilityType: Accessibility;
  accessibility: string;
  time: string;
  place: string;
};

export const LiveEvent = ({
  id,
  img,
  title,
  price,
  discount,
  accessibilityType,
  accessibility,
  time,
  place,
}: LiveEventProps) => {
  return (
    <StyledBox>
      <StyledPaper elevation={1}>
        <Link to={`/events/${id}`}>
          <StyledImg src={img} />
        </Link>
        <Labels>
          <ColoredChip label={price} />
          <GrayChip label={discount} />
          <AccessibilityChip label={accessibility} ac={accessibilityType} />
        </Labels>
        <Stack>
          <Typography variant="body1">{title}</Typography>
          <Typography variant="body2">{time}</Typography>
          <Typography variant="body2">{place}</Typography>
        </Stack>
      </StyledPaper>
    </StyledBox>
  );
};
