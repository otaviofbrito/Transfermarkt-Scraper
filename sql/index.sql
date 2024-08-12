CREATE INDEX idx_player ON players (id);

CREATE INDEX idx_transfer ON players (player_id, year, left_club_id, joined_club_id);

CREATE INDEX idx_leagues ON players (id);

CREATE INDEX idx_clubs ON clubs (id);

CREATE INDEX idx_club_league ON club_league (club_id, league_id, season);
