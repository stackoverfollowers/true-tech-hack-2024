import { axios } from '@shared/api';
import { EventsResponse } from '@shared/types/events';
import { Pagination } from '@shared/types/pagination';
import { useQuery } from '@tanstack/react-query';

const queryKey = ['events'];
const endpointKey = '/events';

const getEvents = async ({ signal }: { signal: AbortSignal }) => {
  const { data } = await axios(endpointKey, {
    signal,
  });

  return data;
};

const getEventById = async (id: number, { signal }: { signal: AbortSignal }) => {
  const { data } = await axios(`${endpointKey}/${id}`, {
    signal,
  });

  return data;
};

export const useGetEventById = (id: number) => {
  return useQuery<EventsResponse>({
    queryKey,
    queryFn: ({ signal} ) => getEventById(id, {signal}),
  });
};

type UseGetEvents = Pagination<EventsResponse[]>;

export const useGetEvents = () => {
  return useQuery<UseGetEvents>({
    queryKey,
    queryFn: getEvents,
  });
};

