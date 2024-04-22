export type HistoricalSite = {
  id: number;
  name: string;
  description: string;
  latitude: number;
  longitude: number;
  address: string;
  era: string;
  tags: string[];
  images: string[];
  audio_guide_url?: string;
  verified: boolean;
};

export type Contribution = {
  id: number;
  site_id: number;
  user_id: number;
  text: string;
  images: string[];
  audio?: string;
  verified: boolean;
};