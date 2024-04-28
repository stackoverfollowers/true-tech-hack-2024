type Event = {
  title: string;
  img: string;
  place: string;
  rating: string;
  accessibility: string;
};

type EventsResponse = {
  id: number;
  place_id: number;
  name: string;
  description: string;
};

export type { Event, EventsResponse };
