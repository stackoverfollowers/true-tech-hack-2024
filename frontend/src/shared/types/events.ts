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
  event_type: string;
  url: string;
  image_url: string;
  description: null;
  started_at: null;
  ended_at: null;
  created_at: string;
  updated_at: string;
  features: {
    name: string,
    slug: string,
    value: string
  }[]
};

export type { Event, EventsResponse };
