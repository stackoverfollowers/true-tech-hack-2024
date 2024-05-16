import { useGetEventById } from '@entities/event/api';
import { Box, Button, Chip, Container } from '@mui/material';
import { AccessibilityChip } from '@widgets/accessibility-chip';
import { useParams } from 'react-router-dom';

import styles from './styles.module.css';
import { useGetPlaceById } from '@entities/places/api';


const dummy_place = {
  "id": 559890,
  "name": "Театр «Алеко»",
  "url": "https://live.mts.ru/sankt-peterburg/venues/theater/teatr-aleko",
  "image_url": "https://live.mts.ru/image/venues/teatr-aleko-3a9480d2-8ca0-4f32-8674-aaf995e7d0f3.jpg",
  "description": null,
  "address": "Санкт-Петербург, пр. Юрия Гагарина, 42",
  "created_at": "2024-05-13T05:00:02.200510Z",
  "updated_at": "2024-05-13T05:00:02.200511Z",
  "features": []
}

export const EventPage = () => {
  const { id } = useParams();

  const { data } = useGetEventById(Number(id));

  const { data: place } = useGetPlaceById(data?.place_id);

  if (!data) return null;

  const { name, description, image_url } = data;

  return (
    <Container>
      <div className={styles.grid}>
        <div className={styles.inner}>
          <img src={image_url} className={styles.img} />
        </div>
        <div className={styles.stack}>
          <Box component='h1' sx={{ color: 'text.primary' }} className={styles.name}>
            {name}
          </Box>
          <Box sx={{ color: 'text.primary' }} className={styles.place}>
            {place?.name || dummy_place.name}
          </Box>
          {data.features && data.features.length > 0 && (
            <div className={styles.chips}>
              {data.features.map((feature, idx) => (
                <AccessibilityChip
                  key={idx}
                  label={feature.name}
                  ac={feature.value === 'AVAILABLE' ? 'Good' : 'Neutral'}
                  size='small'
                />
              ))}
              <Chip label="Open Air" size='small' />
              <Chip label="16+" size='small' />
            </div>
          )}
          <Button variant="contained" style={{ backgroundColor: '#ff0032' }}>Купить билет</Button>
        </div>
      </div>


      <div className={styles.desc}>
        <h2 className={styles.title}>Описание</h2>
        <div>
          <Box sx={{ color: 'text.primary' }}>
            {name}
          </Box>

          <Box sx={{ color: 'text.primary' }} className={styles.description}>
            {description || (
              <>
                <p>
                  {name} - это удивительное произведение, которое завоевало сердца зрителей по всему миру. Созданное в результате творческого сотрудничества талантливых художников, оно представляет собой уникальное сочетание искусства и эмоций.
                </p>
                <p>
                  Впервые представленное публике в далеком году, {name} до сих пор остается актуальным и захватывающим для зрителей. В новой интерпретации события, режиссер возвращает к его первоначальной задумке, сохраняя его уникальный характер и глубокий смысл. Авторы события вносят в него новые элементы, обогащая его духовностью, фольклором и современными музыкальными тенденциями.
                  {name} - это истинное произведение искусства, которое продолжает вдохновлять и радовать публику своей красотой и глубиной.
                </p>
              </>
            )}
          </Box>
        </div>
      </div>

    </Container>
  );
};
