import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CollegesModule } from './colleges/colleges.module';
import {PlayersModule} from "./players/players.module";

@Module({
  imports: [CollegesModule, PlayersModule],
  controllers: [AppController],
  providers: [AppService],
})

export class AppModule {}
