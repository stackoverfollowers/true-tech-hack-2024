import { useCreatePlace } from '@entities/places/api';
import { Button, Dialog, Input, styled } from '@mui/material';
import { CreatePlaceDTO } from '@shared/types/places';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

type CreatePlaceModalProps = {
  open: boolean;
  onClose: () => void;
};

const Paper = styled('div')({
  padding: 30,
  display: 'flex',
  flexDirection: 'column',
  rowGap: 10,
  minWidth: 500,
});

const StyledTextField = styled(Input)({
  fontSize: 20,
});

const StyledButton = styled(Button)({
  fontSize: 16,
  marginTop: 20,
});

const Wrapper = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  border: '1px solid #ccc',
  padding: 10,
});

export const CreatePlaceModal = ({ open, onClose }: CreatePlaceModalProps) => {
  const [place, setPlace] = useState<CreatePlaceDTO>({
    name: '',
    url: '',
    image_url: '',
    description: '',
    address: '',
  });

  const navigate = useNavigate();

  const { mutateAsync: createPlace } = useCreatePlace();

  const onChange = (key: keyof CreatePlaceDTO, value: string) => {
    setPlace((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const onCreate = async () => {
    const result = await createPlace(place);

    if (result) {
      onClose();
      navigate(`/places/${result.id}`);
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <Paper>
        <h1>Создание места</h1>
        <Wrapper>
          <label>Название места</label>
          <StyledTextField value={place.name} onChange={(e) => onChange('name', e.target.value)} />
        </Wrapper>
        <Wrapper>
          <label>Адрес места</label>
          <StyledTextField
            value={place.address}
            onChange={(e) => onChange('address', e.target.value)}
          />
        </Wrapper>
        <Wrapper>
          <label>Ссылка на место</label>
          <StyledTextField value={place.url} onChange={(e) => onChange('url', e.target.value)} />
        </Wrapper>
        <Wrapper>
          <label>Ссылка на изображение</label>
          <StyledTextField
            value={place.image_url}
            onChange={(e) => onChange('image_url', e.target.value)}
          />
        </Wrapper>
        <Wrapper>
          <label>Описание места</label>
          <StyledTextField
            value={place.description}
            onChange={(e) => onChange('description', e.target.value)}
          />
        </Wrapper>
        <StyledButton onClick={onCreate} variant="contained">
          Добавить место
        </StyledButton>
      </Paper>
    </Dialog>
  );
};
