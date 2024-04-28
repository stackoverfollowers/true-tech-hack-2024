import { axios } from '@shared/api';
import { EventsResponse } from '@shared/types/events';
import { Pagination } from '@shared/types/pagination';
import { useQuery } from '@tanstack/react-query';

const queryKey = ['events'];
const endpointKey = 'events';

const getEvents = async ({ signal }: { signal: AbortSignal }) => {
  const { data } = await axios(endpointKey, {
    signal,
  });

  return data;
};

type UseGetEvents = Pagination<EventsResponse[]>;

export const useGetEvents = () => {
  return useQuery<UseGetEvents>({
    queryKey,
    queryFn: getEvents,
  });
};
