import { axios } from '@shared/api';
import { Pagination } from '@shared/types/pagination';
import { CreatePlaceDTO, Place } from '@shared/types/places';
import { useMutation, useQuery } from '@tanstack/react-query';

const queryKey = ['places'];
const endpointKey = '/places';

const getPlaces = async ({ signal }: { signal: AbortSignal }) => {
  const { data } = await axios(endpointKey, {
    signal,
  });

  return data;
};

const getPlaceById = async (id: number, { signal }: { signal: AbortSignal }) => {
  const { data } = await axios(`${endpointKey}/${id}`, {
    signal,
  });

  return data;
};

const createPlace = async (place: CreatePlaceDTO) => {
  const { data } = await axios.post<Place>('places', place);

  return data;
};

export const useGetPlaceById = (id: number) => {
  return useQuery<Place>({
    queryKey: [...queryKey, id],
    queryFn: ({ signal }) => getPlaceById(id, { signal }),
    enabled: !!id,
  });
};

type UseGetPlaces = Pagination<Place[]>;

export const useGetPlaces = () => {
  return useQuery<UseGetPlaces>({
    queryKey,
    queryFn: getPlaces,
  });
};

export const useCreatePlace = () => {
  return useMutation<Place, unknown, CreatePlaceDTO>({
    mutationFn: (place: CreatePlaceDTO) => createPlace(place),
  });
};
