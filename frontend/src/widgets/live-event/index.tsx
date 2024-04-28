import { Box, Chip, Grow } from '@mui/material';
import { Accessibility } from '@shared/types/accessibility';
import { AccessibilityChip } from '@widgets/accessibility-chip';
import { Link } from 'react-router-dom';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import { clsx } from 'clsx';
import { forwardRef, useEffect, useState } from 'react';

import styles from './styles.module.css';

export const LiveEvent = forwardRef<Ref, Props>(
  ({ id, img, title, price, discount, accessibilityType, accessibility, time, place }, ref) => {
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
            <div className={styles.cover}>
              <img src={img} className={styles.img} />

              <div className={styles.chips}>
                <Chip label={discount} className={clsx(styles.chip, styles.gray)} />
                <AccessibilityChip label={accessibility} ac={accessibilityType} />
              </div>
            </div>
            <div className={styles.inner}>
              <Box sx={{ color: 'text.secondary' }} className={styles.subtitle}>
                {place}
              </Box>
              <Box sx={{ color: 'text.primary' }} className={styles.title}>
                {title}
              </Box>
              <div className={styles.footer}>
                <div className={styles.time}>
                  <AccessTimeIcon sx={{ width: 16, height: 16 }} />
                  <Box sx={{ color: 'text.secondary' }}>{time}</Box>
                </div>
                <Box sx={{ color: 'text.primary', fontWeight: 500 }}>{price}</Box>
              </div>
            </div>
          </div>
        </Link>
      </Grow>
    );
  },
);

type Ref = HTMLDivElement;

type Props = {
  id: number;
  img: string;
  title: string;
  price: string;
  discount: string;
  accessibilityType: Accessibility;
  accessibility: string;
  time: string;
  place: string;
};
