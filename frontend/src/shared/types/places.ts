type Place = {
  id: number;
  name: string;
  url: string;
  image_url: string;
  description: null;
  address: string;
  created_at: string;
  updated_at: string;
  features: { name: string; slug: string; value: string }[];
};

type CreatePlaceDTO = {
  name: string;
  url: string;
  image_url: string;
  description: string;
  address: string;
};

export type { Place, CreatePlaceDTO };
