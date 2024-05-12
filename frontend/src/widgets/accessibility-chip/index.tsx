import { Chip, styled } from '@mui/material';
import { Accessibility } from '@shared/types/accessibility';

const mapAccessibilityToColor: Record<Accessibility, { backgroundColor: string; color: string }> = {
  Bad: {
    backgroundColor: 'red',
    color: 'white',
  },
  Neutral: {
    backgroundColor: '#F2F3F7',
    color: 'black',
  },
  Good: {
    backgroundColor: '#0dbf1c',
    color: 'white',
  },
};

export const AccessibilityChip = styled(Chip)<{ ac: Accessibility }>((props) => ({
  backgroundColor: mapAccessibilityToColor[props.ac].backgroundColor,
  color: mapAccessibilityToColor[props.ac].color,
  fontSize: 12,
  fontWeight: 500,
  width: 'max-content',
}));
