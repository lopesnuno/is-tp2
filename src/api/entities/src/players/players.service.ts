import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';
import {InsertPlayerDto} from "./dto";

@Injectable()
export class PlayersService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.players.findMany();
    }

    async insertPlayer(dto: InsertPlayerDto): Promise<any> {
        const player = await this.prisma.players.create({
            data: {
                name: dto.name,
                country: dto.country,
                height: dto.height,
                weight: dto.weight,
                draft_year: dto.draft_year,
                draft_round: dto.draft_round,
                draft_number: dto.draft_number,
            }
        })
    }
}