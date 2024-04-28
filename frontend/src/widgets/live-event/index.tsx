import { forwardRef, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Box, Grow } from '@mui/material';

import styles from './styles.module.css';
import { EventsResponse } from '@shared/types/events';

export const LiveEvent = forwardRef<Ref, Props>(({ id, description, name }, ref) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <Grow
      in={mounted}
      style={{ transformOrigin: '0 0 0' }}
      {...(mounted ? { timeout: id * 150 } : {})}
    >
      <Link to="#">
        <div ref={ref} className={styles.card}>
          <div className={styles.inner}>
            <Box sx={{ color: 'text.secondary' }} className={styles.subtitle}>
              {name}
            </Box>
            <Box sx={{ color: 'text.primary' }} className={styles.title}>
              {description}
            </Box>
          </div>
        </div>
      </Link>
    </Grow>
  );
});

type Ref = HTMLDivElement;

type Props = EventsResponse;
