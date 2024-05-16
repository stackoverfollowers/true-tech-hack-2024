import { useGetPlaceById } from '@entities/places/api';
import { Box, Card, Link, Modal } from '@mui/material';

import styles from './styles.module.css';

export const Place = (props: Props) => {
  const { data } = useGetPlaceById(props.placeId);

  return (
    <Modal open={props.open} onClose={props.onClose}>
      <Card className={styles.root}>
        {data && (
          <>
            <Box sx={{ color: 'text.primary' }} className={styles.title}>
              {data.name}
            </Box>
            <div className={styles.cover}>
              <img src={data.image_url} className={styles.img} />
            </div>
            <Box
              component={Link}
              href={data.url}
              sx={{ color: 'text.primary' }}
              className={styles.title}
            >
              Подробнее
            </Box>
          </>
        )}
      </Card>
    </Modal>
  );
};

type Props = {
  open: boolean;
  onClose: () => void;
  placeId: number;
};
