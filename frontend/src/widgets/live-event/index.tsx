import { forwardRef, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Box, Grow } from '@mui/material';
import PushPinIcon from '@mui/icons-material/PushPin';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';

import styles from './styles.module.css';
import { EventsResponse } from '@shared/types/events';
import { Place } from '@widgets/place';
import { AccessibilityChip } from '@widgets/accessibility-chip';

export const LiveEvent = forwardRef<Ref, Props>((props, ref) => {
  const [mounted, setMounted] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <>
      <Grow
        in={mounted}
      >
        <Link to="#">
          <div ref={ref} className={styles.card}>
            <div className={styles.cover}>
              <img src={props.image_url} className={styles.img} />

              {props.features && props.features.length > 0 && <div className={styles.chips}>
                {props.features.map((feature, idx) => (
                  <AccessibilityChip key={idx} label={feature.name} ac={feature.value === 'AVAILABLE' ? 'Good' : 'Neutral'}/>
                ))}
              </div>}
            </div>
            <div className={styles.inner}>
              <Box sx={{ color: 'text.secondary' }} className={styles.subtitle}>
                {props.event_type}
              </Box>
              <Box sx={{ color: 'text.primary' }} className={styles.title}>
                {props.name}
              </Box>
              <Box sx={{ color: 'text.primary' }} className={styles.description}>
                {props.description || 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'}
              </Box>
              <div className={styles.footer}>
                <div className={styles.time}>
                  <CalendarMonthIcon sx={{ width: 16, height: 16 }} />
                  <Box sx={{ color: 'text.secondary' }}>{new Intl.DateTimeFormat('ru-RU', {
                    dateStyle: 'medium',
                  }).format(new Date(props.created_at))}</Box>
                </div>
                <div className={styles.place} onClick={() => setIsOpen(true)}>
                  <PushPinIcon sx={{ width: 16, height: 16, color: 'text.secondary' }} />
                  <Box sx={{ color: 'text.secondary' }}>{props.place_id}</Box>
                </div>
              </div>
            </div>
          </div>
        </Link>
      </Grow>
      <Place placeId={props.place_id} open={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
});

type Ref = HTMLDivElement;

type Props = EventsResponse;
