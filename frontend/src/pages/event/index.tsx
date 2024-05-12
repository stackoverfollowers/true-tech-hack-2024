import { useGetEventById } from '@entities/event/api';
import { Box, Container } from '@mui/material';
import { AccessibilityChip } from '@widgets/accessibility-chip';
import { useParams } from 'react-router-dom';

import styles from './styles.module.css';

export const EventPage = () => {
  const { id } = useParams();

  const { data } = useGetEventById(Number(id));

  if (!data) return null;

  const { name, event_type, description, image_url } = data;

  return (
    <Container>
      <Box sx={{ color: 'text.secondary' }} className={styles.subtitle}>
        {event_type}
      </Box>
      <Box sx={{ color: 'text.primary' }} className={styles.title}>
        {name}
      </Box>
      <Box sx={{ color: 'text.primary' }} className={styles.description}>
        {description ||
          'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'}
      </Box>
      <img src={image_url} className={styles.img} />
      {data.features && data.features.length > 0 && (
        <div className={styles.chips}>
          {data.features.map((feature, idx) => (
            <AccessibilityChip
              key={idx}
              label={feature.name}
              ac={feature.value === 'AVAILABLE' ? 'Good' : 'Neutral'}
            />
          ))}
        </div>
      )}
    </Container>
  );
};
