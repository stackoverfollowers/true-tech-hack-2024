import { axios } from '@shared/api';
import { Pagination } from '@shared/types/pagination';
import { Place } from '@shared/types/places';
import { useQuery } from '@tanstack/react-query';

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

export const useGetPlaceById = (id: number) => {
  return useQuery<Place>({
    queryKey,
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
