import { useGetEvents } from '@entities/event/api';
import { Container, Typography, styled } from '@mui/material';
import { LiveEvent } from '@widgets/live-event';

const Title = styled(Typography)({
  fontSize: '2rem',
  fontWeight: '600',
});

const StyledContainer = styled(Container)({
  padding: 10,
});

const Cards = styled('div')(() => ({
  display: 'flex',
  flexWrap: 'wrap',
  margin: '0 -8px',
}));

const Wrapper = styled('div')(({ theme }) => ({
  position: 'relative',
  marginTop: theme.spacing(3),
  width: '100%',
  minHeight: '1px',
  paddingInline: theme.spacing(1),
  flex: '0 0 100%',
  maxWidth: '100%',

  [theme.breakpoints.up('sm')]: {
    flex: '0 0 50%',
    maxWidth: '50%',
  },

  [theme.breakpoints.up('md')]: {
    flex: '0 0 33.333333%',
    maxWidth: '33.333333%',
  },
}));

const data = {
  "meta": {
    "total": 11241,
    "limit": 20,
    "offset": 0
  },
  "items": [
    {
      "id": 2836215,
      "place_id": 559890,
      "name": "Спектакль «Золотой ключик»",
      "event_type": "children",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/zolotoy-klyuchik_48?eventId=18699805",
      "image_url": "https://live.mts.ru/image/536x360/zolotoy-klyuchik_48-c62e067c-d136-4e52-9cd2-ac5a620e18b3.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:18.043847Z",
      "updated_at": "2024-05-13T05:00:18.043848Z"
    },
    {
      "id": 2836232,
      "place_id": 559896,
      "name": "Спектакль «Эта прекрасная жизнь»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/eta-prekrasnaya-zhizn?eventId=18647731",
      "image_url": "https://live.mts.ru/image/536x360/eta-prekrasnaya-zhizn-4e478859-3955-4def-901b-0105edea17c9.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738947Z",
      "updated_at": "2024-05-13T05:00:16.738948Z"
    },
    {
      "id": 2836236,
      "place_id": 559898,
      "name": "Спектакль «Соломенная шляпка»",
      "event_type": "theater",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/spektakl-solomennaya-shlyapka?eventId=18741410",
      "image_url": "https://live.mts.ru/image/536x360/spektakl-solomennaya-shlyapka-165f8556-d99f-4c2e-9690-7806afd98e1f.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:17.710789Z",
      "updated_at": "2024-05-13T05:00:17.710790Z"
    },
    {
      "id": 2836249,
      "place_id": 559895,
      "name": "Спектакль «Женитьба?»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/wedding?eventId=18730827",
      "image_url": "https://live.mts.ru/image/536x360/wedding-70d0755a-67df-46b6-81d6-2df06eb38eec.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738948Z",
      "updated_at": "2024-05-13T05:00:16.738949Z"
    },
    {
      "id": 2836256,
      "place_id": 559895,
      "name": "Спектакль «Царский путь»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/spektaklcarskiy-put?eventId=18675081",
      "image_url": "https://live.mts.ru/image/536x360/spektaklcarskiy-put-0c9392c1-b704-448a-aa55-d167d962130d.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738950Z",
      "updated_at": "2024-05-13T05:00:16.738951Z"
    },
    {
      "id": 2836259,
      "place_id": 559903,
      "name": "Спектакль «Мастер и Маргарита»",
      "event_type": "theater",
      "url": "https://live.mts.ru/kemerovo/announcements/master-i-margarita?eventId=18743806",
      "image_url": "https://live.mts.ru/image/536x360/master-i-margarita-8f30fe63-0bf7-43be-9bce-302b29b86577.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T06:30:18.243412Z",
      "updated_at": "2024-05-13T06:30:18.243413Z"
    },
    {
      "id": 2836272,
      "place_id": 559898,
      "name": "Спектакль «Вишнёвый сад»",
      "event_type": "theater",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/spektakl-vishnyovyy-sad?eventId=18683341",
      "image_url": "https://live.mts.ru/image/536x360/spektakl-vishnyovyy-sad-a275ae65-9d21-49ec-93a5-761dab869f5e.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:17.710791Z",
      "updated_at": "2024-05-13T05:00:17.710792Z"
    },
    {
      "id": 2836273,
      "place_id": 559893,
      "name": "Спектакль «Спящая красавица»",
      "event_type": "children",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/spyaschaya-krasavica_50?eventId=18722812",
      "image_url": "https://live.mts.ru/image/536x360/spyaschaya-krasavica_50-6aca1868-7160-4138-a748-4045dff6f063.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:18.043849Z",
      "updated_at": "2024-05-13T05:00:18.043849Z"
    },
    {
      "id": 2836275,
      "place_id": 559905,
      "name": "Концерт Софи Окран",
      "event_type": "concerts",
      "url": "https://live.mts.ru/moscow/announcements/sofi-okran-rossiya?eventId=18689978",
      "image_url": "https://live.mts.ru/image/536x360/sofi-okran-rossiya-9c282182-f6e4-4c0c-ac6c-e25e3287b018.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.354060Z",
      "updated_at": "2024-05-13T05:00:16.354061Z"
    },
    {
      "id": 2836277,
      "place_id": 559905,
      "name": "Концерт Виктора Зинчука",
      "event_type": "concerts",
      "url": "https://live.mts.ru/moscow/announcements/koncert-viktor-zinchuk?eventId=18651213",
      "image_url": "https://live.mts.ru/image/536x360/koncert-viktor-zinchuk-eb6c37e0-3309-4424-b8bc-41499df33ae9.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.354090Z",
      "updated_at": "2024-05-13T05:00:16.354091Z"
    },
    {
      "id": 2836279,
      "place_id": 559893,
      "name": "Спектакль «И. Конвенан. Любимая игрушка»",
      "event_type": "children",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/i-konvenan-lyubimaya-igrushka?eventId=18695536",
      "image_url": "https://live.mts.ru/image/536x360/i-konvenan-lyubimaya-igrushka-52223a82-1f27-4828-a2f4-f4544aff8764.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:18.043850Z",
      "updated_at": "2024-05-13T05:00:18.043851Z"
    },
    {
      "id": 2836295,
      "place_id": 559912,
      "name": "Спектакль «Доктор знает всё»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/doktor-znaet-vsyo_276?eventId=18677823",
      "image_url": "https://live.mts.ru/image/536x360/doktor-znaet-vsyo_276-0f394a89-c01b-40c0-8995-34da91f8d4ad.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738952Z",
      "updated_at": "2024-05-13T05:00:16.738953Z"
    },
    {
      "id": 2836302,
      "place_id": 559901,
      "name": "Спектакль «Три поросёнка и серый волк»",
      "event_type": "children",
      "url": "https://live.mts.ru/moscow/announcements/spektakl-tri-porosyonka-i-seryy-volk?eventId=18568239",
      "image_url": "https://live.mts.ru/image/536x360/spektakl-tri-porosyonka-i-seryy-volk-db1863c2-adc6-47f1-8527-b8b5190592d2.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T17:30:19.957774Z",
      "updated_at": "2024-05-13T17:30:19.957776Z"
    },
    {
      "id": 2836307,
      "place_id": 559901,
      "name": "Спектакль «О дивный новый мир»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/spektakl-o-divnyy-novyy-mir?eventId=18678124",
      "image_url": "https://live.mts.ru/image/536x360/spektakl-o-divnyy-novyy-mir-16b8ced0-66c2-40f4-87ac-5f94a65231f6.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738954Z",
      "updated_at": "2024-05-13T05:00:16.738955Z"
    },
    {
      "id": 2836324,
      "place_id": 559898,
      "name": "Спектакль «Баба Шанель»",
      "event_type": "theater",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/spektakl-baba-shanel?eventId=18683333",
      "image_url": "https://live.mts.ru/image/536x360/spektakl-baba-shanel-a7673b27-ef42-47d7-92ac-1e4f4593783d.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:17.710793Z",
      "updated_at": "2024-05-13T05:00:17.710794Z"
    },
    {
      "id": 2836326,
      "place_id": 559920,
      "name": "Спектакль «Мальва»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/malva?eventId=18700309",
      "image_url": "https://live.mts.ru/image/536x360/malva-aab7d251-b0da-402e-90b9-bf90fe15c306.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738956Z",
      "updated_at": "2024-05-13T05:00:16.738957Z"
    },
    {
      "id": 2836355,
      "place_id": 559901,
      "name": "Спектакль «Затерянный мир»",
      "event_type": "children",
      "url": "https://live.mts.ru/moscow/announcements/zateryannyy-mir?eventId=18678129",
      "image_url": "https://live.mts.ru/image/536x360/zateryannyy-mir-049e6e5f-7d99-4be2-a7f7-906a012cd013.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:17.333617Z",
      "updated_at": "2024-05-13T05:00:17.333618Z"
    },
    {
      "id": 2836359,
      "place_id": 559930,
      "name": "Спектакль «Блажь»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/blazh_11?eventId=18673544",
      "image_url": "https://live.mts.ru/image/536x360/blazh_11-acc22956-8940-48a1-8fa2-662ae18982f6.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738958Z",
      "updated_at": "2024-05-13T05:00:16.738958Z"
    },
    {
      "id": 2836366,
      "place_id": 559933,
      "name": "Спектакль «Вишневый сад»",
      "event_type": "theater",
      "url": "https://live.mts.ru/moscow/announcements/vishnevyy-sad_46?eventId=18686203",
      "image_url": "https://live.mts.ru/image/536x360/vishnevyy-sad_46-ee6d8f05-16f0-4b12-8d6a-c6057dbac972.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:16.738959Z",
      "updated_at": "2024-05-13T05:00:16.738960Z"
    },
    {
      "id": 2836370,
      "place_id": 559898,
      "name": "Спектакль «Шутники»",
      "event_type": "theater",
      "url": "https://live.mts.ru/sankt-peterburg/announcements/shutniki-16?eventId=18683334",
      "image_url": "https://live.mts.ru/image/536x360/shutniki-16-63a44c12-3315-4865-b371-d003588060d4.jpg",
      "description": null,
      "started_at": null,
      "ended_at": null,
      "created_at": "2024-05-13T05:00:17.710794Z",
      "updated_at": "2024-05-13T05:00:17.710795Z"
    }
  ]
}

export const RootPage = () => {
  // const { data } = useGetEvents();

  // console.log('data', data)

  return (
    <>
      <StyledContainer>
        <Title variant="h2">Афиша Санкт-Петербурга</Title>
      </StyledContainer>
      <StyledContainer>
        <Cards>
          {data?.items.map((item, idx) => (
            <Wrapper key={idx}>
              <LiveEvent {...item} />
            </Wrapper>
          ))}
        </Cards>
      </StyledContainer>
    </>
  );
};
