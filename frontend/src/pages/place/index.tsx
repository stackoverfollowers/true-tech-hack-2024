import { Box, Button, Chip, Paper, styled } from '@mui/material';
import { useGetPlaceById } from '@entities/places/api';
import { AccessibilityChip } from '@widgets/accessibility-chip';
import { useParams } from 'react-router-dom';

import styles from './styles.module.css';

const StyledPaper = styled(Paper)({
  maxWidth: 1200,
  alignSelf: 'center',
  padding: 30,
});

export const PlacePage = () => {
  const { id } = useParams();

  const { data } = useGetPlaceById(Number(id));

  if (!data) return null;

  const { name, description, image_url } = data;

  const features =
    data.features.length > 0 ? data.features : [{ name: 'Пандус', value: 'AVAILABLE' }];

  return (
    <StyledPaper elevation={6}>
      <div className={styles.grid}>
        <div className={styles.inner}>
          <img src={image_url} className={styles.img} />
        </div>
        <div className={styles.stack}>
          <Box component="h1" sx={{ color: 'text.primary' }} className={styles.name}>
            {name}
          </Box>
          <Box sx={{ color: 'text.primary' }} className={styles.place}>
            {data.address}
          </Box>
          <div className={styles.chips}>
            {features.map((feature, idx) => (
              <AccessibilityChip
                key={idx}
                label={feature.name}
                ac={feature.value === 'AVAILABLE' ? 'Good' : 'Neutral'}
                size="small"
              />
            ))}
            <Chip label="Open Air" size="small" />
            <Chip label="16+" size="small" />
          </div>
          <Button variant="contained" style={{ backgroundColor: '#ff0032' }}>
            Купить билет
          </Button>
          <div className={styles.desc}>
            <h2 className={styles.title}>Описание</h2>
            <div>
              <Box sx={{ color: 'text.primary' }}>{name}</Box>

              <Box sx={{ color: 'text.primary' }} className={styles.description}>
                {description || (
                  <>
                    <p>
                      {name} - это удивительное произведение, которое завоевало сердца зрителей по
                      всему миру. Созданное в результате творческого сотрудничества талантливых
                      художников, оно представляет собой уникальное сочетание искусства и эмоций.
                    </p>
                    <p>
                      Впервые представленное публике в далеком году, {name} до сих пор остается
                      актуальным и захватывающим для зрителей. В новой интерпретации события,
                      режиссер возвращает к его первоначальной задумке, сохраняя его уникальный
                      характер и глубокий смысл. Авторы события вносят в него новые элементы,
                      обогащая его духовностью, фольклором и современными музыкальными тенденциями.
                      {name} - это истинное произведение искусства, которое продолжает вдохновлять и
                      радовать публику своей красотой и глубиной.
                    </p>
                  </>
                )}
              </Box>
            </div>
          </div>
        </div>
      </div>
    </StyledPaper>
  );
};
