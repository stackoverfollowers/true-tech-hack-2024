export type Pagination<Type> = {
  meta: {
    total: number;
    limit: number;
    offser: number;
  };
  items: Type;
};
